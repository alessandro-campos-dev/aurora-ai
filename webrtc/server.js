// WebRTC Signaling Server para Telemedicina Aurora AI
// Usando WebSocket para signaling e media server

const WebSocket = require('ws');
const https = require('https');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

// Configurações
const PORT = process.env.PORT || 8443;
const SSL_CERT = process.env.SSL_CERT || './ssl/cert.pem';
const SSL_KEY = process.env.SSL_KEY || './ssl/key.pem';

// Mapa para armazenar salas e conexões
const rooms = new Map();
const connections = new Map();

// Verifica SSL para produção
let server;
if (fs.existsSync(SSL_CERT) && fs.existsSync(SSL_KEY)) {
    const options = {
        cert: fs.readFileSync(SSL_CERT),
        key: fs.readFileSync(SSL_KEY)
    };
    server = https.createServer(options);
    console.log('🔐 Servidor HTTPS iniciado');
} else {
    console.log('⚠️ SSL não encontrado, iniciando servidor HTTP para desenvolvimento');
    server = require('http').createServer();
}

// WebSocket Server
const wss = new WebSocket.Server({ server });

// Eventos de conexão WebSocket
wss.on('connection', (ws, req) => {
    const connectionId = uuidv4();
    connections.set(connectionId, {
        ws,
        roomId: null,
        userId: null,
        userType: null, // 'medico' ou 'paciente'
        metadata: {}
    });
    
    console.log(`🔄 Nova conexão: ${connectionId} (Total: ${connections.size})`);
    
    // Mensagem de boas-vindas
    sendTo(ws, {
        type: 'welcome',
        connectionId,
        timestamp: new Date().toISOString(),
        server: 'Aurora AI WebRTC',
        version: '1.0.0'
    });
    
    // Handler de mensagens
    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            handleMessage(connectionId, data);
        } catch (error) {
            console.error('❌ Erro ao processar mensagem:', error);
            sendError(ws, 'invalid_message', 'Mensagem inválida');
        }
    });
    
    // Handler de desconexão
    ws.on('close', () => {
        const connection = connections.get(connectionId);
        if (connection && connection.roomId) {
            leaveRoom(connectionId, connection.roomId);
        }
        connections.delete(connectionId);
        console.log(`👋 Conexão fechada: ${connectionId} (Total: ${connections.size})`);
    });
    
    // Handler de erros
    ws.on('error', (error) => {
        console.error(`💥 Erro na conexão ${connectionId}:`, error);
    });
});

// Função para lidar com mensagens
function handleMessage(connectionId, data) {
    const connection = connections.get(connectionId);
    if (!connection) return;
    
    const { ws } = connection;
    
    console.log(`📨 ${connectionId}: ${data.type}`);
    
    switch (data.type) {
        case 'join':
            handleJoin(connectionId, data);
            break;
            
        case 'offer':
        case 'answer':
        case 'ice-candidate':
            handleWebRTC(connectionId, data);
            break;
            
        case 'chat':
            handleChat(connectionId, data);
            break;
            
        case 'recording':
            handleRecording(connectionId, data);
            break;
            
        case 'presence':
            handlePresence(connectionId, data);
            break;
            
        case 'disconnect':
            handleDisconnect(connectionId, data);
            break;
            
        default:
            sendError(ws, 'unknown_type', 'Tipo de mensagem desconhecido');
    }
}

// Handler: Entrar em uma sala
function handleJoin(connectionId, data) {
    const connection = connections.get(connectionId);
    const { roomId, userId, userType, metadata } = data;
    
    if (!roomId || !userId || !userType) {
        sendError(connection.ws, 'invalid_join', 'Dados de entrada inválidos');
        return;
    }
    
    // Verifica se a sala existe, caso contrário cria
    if (!rooms.has(roomId)) {
        rooms.set(roomId, {
            id: roomId,
            participants: new Map(),
            createdAt: new Date(),
            metadata: {}
        });
        console.log(`🚪 Sala criada: ${roomId}`);
    }
    
    const room = rooms.get(roomId);
    
    // Verifica se usuário já está na sala
    if (room.participants.has(userId)) {
        sendError(connection.ws, 'user_exists', 'Usuário já está na sala');
        return;
    }
    
    // Atualiza conexão
    connection.roomId = roomId;
    connection.userId = userId;
    connection.userType = userType;
    connection.metadata = metadata || {};
    
    // Adiciona à sala
    room.participants.set(userId, {
        connectionId,
        userId,
        userType,
        joinedAt: new Date(),
        metadata: connection.metadata
    });
    
    // Notifica entrada bem-sucedida
    sendTo(connection.ws, {
        type: 'joined',
        roomId,
        userId,
        userType,
        timestamp: new Date().toISOString()
    });
    
    // Notifica outros participantes
    broadcastToRoom(roomId, connectionId, {
        type: 'user-joined',
        userId,
        userType,
        metadata: connection.metadata,
        timestamp: new Date().toISOString()
    });
    
    // Envia lista de participantes existentes
    const participants = Array.from(room.participants.values())
        .filter(p => p.userId !== userId)
        .map(p => ({
            userId: p.userId,
            userType: p.userType,
            metadata: p.metadata
        }));
    
    if (participants.length > 0) {
        sendTo(connection.ws, {
            type: 'existing-users',
            participants,
            timestamp: new Date().toISOString()
        });
    }
    
    console.log(`✅ ${userId} (${userType}) entrou na sala ${roomId}`);
}

// Handler: Mensagens WebRTC (offer, answer, ice-candidate)
function handleWebRTC(connectionId, data) {
    const connection = connections.get(connectionId);
    if (!connection || !connection.roomId) return;
    
    const { targetUserId, ...messageData } = data;
    
    // Encontra conexão do target
    const room = rooms.get(connection.roomId);
    if (!room) return;
    
    const targetParticipant = room.participants.get(targetUserId);
    if (!targetParticipant) {
        sendError(connection.ws, 'user_not_found', 'Usuário alvo não encontrado');
        return;
    }
    
    const targetConnection = connections.get(targetParticipant.connectionId);
    if (!targetConnection) return;
    
    // Encaminha mensagem WebRTC
    sendTo(targetConnection.ws, {
        ...messageData,
        fromUserId: connection.userId,
        timestamp: new Date().toISOString()
    });
}

// Handler: Mensagens de chat
function handleChat(connectionId, data) {
    const connection = connections.get(connectionId);
    if (!connection || !connection.roomId) return;
    
    const { message, messageType = 'text' } = data;
    
    broadcastToRoom(connection.roomId, connectionId, {
        type: 'chat-message',
        fromUserId: connection.userId,
        fromUserType: connection.userType,
        message,
        messageType,
        timestamp: new Date().toISOString()
    });
}

// Handler: Controle de gravação
function handleRecording(connectionId, data) {
    const connection = connections.get(connectionId);
    if (!connection || !connection.roomId) return;
    
    const { action, recordingId, url } = data;
    
    // Verifica se é médico (apenas médicos podem controlar gravação)
    if (connection.userType !== 'medico') {
        sendError(connection.ws, 'unauthorized', 'Apenas médicos podem controlar gravações');
        return;
    }
    
    broadcastToRoom(connection.roomId, null, {
        type: 'recording-control',
        action,
        recordingId,
        url,
        fromUserId: connection.userId,
        timestamp: new Date().toISOString()
    });
}

// Handler: Presença (heartbeat, status)
function handlePresence(connectionId, data) {
    const connection = connections.get(connectionId);
    if (!connection || !connection.roomId) return;
    
    const { status } = data;
    
    // Atualiza último heartbeat
    connection.lastHeartbeat = Date.now();
    
    // Notifica sala sobre status (opcional, para features avançadas)
    if (status) {
        broadcastToRoom(connection.roomId, connectionId, {
            type: 'user-status',
            userId: connection.userId,
            status,
            timestamp: new Date().toISOString()
        });
    }
}

// Handler: Desconectar de sala
function handleDisconnect(connectionId, data) {
    const connection = connections.get(connectionId);
    if (connection && connection.roomId) {
        leaveRoom(connectionId, connection.roomId);
    }
}

// Função para sair de uma sala
function leaveRoom(connectionId, roomId) {
    const connection = connections.get(connectionId);
    const room = rooms.get(roomId);
    
    if (!connection || !room) return;
    
    const userId = connection.userId;
    
    // Remove da sala
    room.participants.delete(userId);
    
    // Limpa dados da conexão
    connection.roomId = null;
    connection.userId = null;
    connection.userType = null;
    
    // Notifica outros participantes
    broadcastToRoom(roomId, connectionId, {
        type: 'user-left',
        userId,
        timestamp: new Date().toISOString()
    });
    
    // Limpa sala se estiver vazia
    if (room.participants.size === 0) {
        rooms.delete(roomId);
        console.log(`🗑️ Sala removida: ${roomId}`);
    }
    
    console.log(`👋 ${userId} saiu da sala ${roomId}`);
}

// Função para broadcast em uma sala
function broadcastToRoom(roomId, excludeConnectionId, message) {
    const room = rooms.get(roomId);
    if (!room) return;
    
    room.participants.forEach((participant) => {
        if (participant.connectionId !== excludeConnectionId) {
            const conn = connections.get(participant.connectionId);
            if (conn && conn.ws.readyState === WebSocket.OPEN) {
                sendTo(conn.ws, message);
            }
        }
    });
}

// Função auxiliar para enviar mensagens
function sendTo(ws, data) {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
    }
}

// Função para enviar erros
function sendError(ws, code, message) {
    sendTo(ws, {
        type: 'error',
        code,
        message,
        timestamp: new Date().toISOString()
    });
}

// Health check endpoint
if (server !== wss) {
    server.on('request', (req, res) => {
        if (req.url === '/health') {
            res.writeHead(200);
            res.end(JSON.stringify({
               
