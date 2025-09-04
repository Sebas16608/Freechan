console.log('✅ board.js cargado');

// Configuración
const API_BASE_URL = 'http://localhost:1900';

// Obtener ID del board de la URL
const urlParams = new URLSearchParams(window.location.search);
const boardId = urlParams.get('id');

console.log('Board ID from URL:', boardId);

// Elementos del DOM
const boardHeader = document.getElementById('board-header');
const threadsList = document.getElementById('threads-list');
const threadsLoading = document.getElementById('threads-loading');
const threadsError = document.getElementById('threads-error');
const createThreadForm = document.getElementById('create-thread-form');

// Inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Iniciando página de board');
    
    if (!boardId) {
        showError('No se especificó el board en la URL');
        return;
    }
    
    loadBoard();
    loadThreads();
    
    if (createThreadForm) {
        createThreadForm.addEventListener('submit', handleCreateThread);
    }
});

// Cargar datos del board
async function loadBoard() {
    try {
        console.log('📋 Cargando board con ID:', boardId);
        const response = await fetch(`${API_BASE_URL}/api/boards/${boardId}`);
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const board = await response.json();
        console.log('✅ Board recibido:', board);
        displayBoardHeader(board);
        
    } catch (error) {
        console.error('❌ Error cargando board:', error);
        showError('Error cargando board: ' + error.message);
    }
}

// Mostrar información del board
function displayBoardHeader(board) {
    boardHeader.innerHTML = `
        <div class="hero">
            <h2>${board.short_name} - ${board.titulo}</h2>
            <p>${board.descripcion || 'Sin descripción'}</p>
            ${board.featured ? '<span class="featured-badge">⭐ Board destacado</span>' : ''}
        </div>
    `;
}

// Cargar threads del board
async function loadThreads() {
    showThreadsLoading();
    hideThreadsError();
    
    try {
        console.log('🧵 Cargando threads...');
        const response = await fetch(`${API_BASE_URL}/api/threads`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const allThreads = await response.json();
        console.log('📦 Todos los threads:', allThreads);
        
        // Filtrar threads por board_id
        const boardThreads = allThreads.filter(thread => 
            thread.board_id && parseInt(thread.board_id) === parseInt(boardId)
        );
        
        console.log('✅ Threads del board:', boardThreads);
        displayThreads(boardThreads);
        
    } catch (error) {
        console.error('❌ Error cargando threads:', error);
        showThreadsError('Error cargando threads: ' + error.message);
    } finally {
        hideThreadsLoading();
    }
}

// Mostrar threads
function displayThreads(threads) {
    console.log('🎨 Mostrando', threads.length, 'threads');
    
    if (threads.length === 0) {
        threadsList.innerHTML = `
            <div class="no-threads">
                <p>📭 No hay threads en este board</p>
                <p><small>Sé el primero en crear un thread!</small></p>
            </div>
        `;
        return;
    }
    
    threadsList.innerHTML = threads.map(thread => `
        <div class="thread-item" onclick="viewThread(${thread.id})">
            <div class="thread-header">
                <h4 class="thread-title">${thread.titulo || 'Sin título'}</h4>
                <span class="thread-meta">${formatDate(thread.created)}</span>
            </div>
            <div class="thread-content">
                ${thread.contenido ? thread.contenido.substring(0, 150) + '...' : 'Sin contenido'}
            </div>
            <div class="thread-footer">
                <span class="thread-stats">📅 ${formatDate(thread.created)}</span>
                <span class="thread-stats">⭐ ${thread.featured ? 'Destacado' : 'Normal'}</span>
            </div>
        </div>
    `).join('');
}

// Crear nuevo thread
async function handleCreateThread(event) {
    event.preventDefault();
    
    const title = document.getElementById('thread-title').value;
    const content = document.getElementById('thread-content').value;
    
    if (!title || !content) {
        alert('Por favor completa todos los campos');
        return;
    }
    
    try {
        console.log('➕ Creando thread...');
        
        const response = await fetch(`${API_BASE_URL}/api/threads`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                titulo: title,
                contenido: content,
                board_id: parseInt(boardId),
                featured: false
            })
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('✅ Thread creado:', result);
        
        alert('Thread creado exitosamente!');
        document.getElementById('create-thread-form').reset();
        loadThreads();
        
    } catch (error) {
        console.error('❌ Error creando thread:', error);
        alert('Error creando thread: ' + error.message);
    }
}

// Navegación
function viewThread(threadId) {
    console.log('🔗 Navegando al thread:', threadId);
    window.location.href = `thread.html?id=${threadId}`;
}

function goBack() {
    window.location.href = 'index.html';
}

// Utilidades
function formatDate(dateString) {
    if (!dateString) return 'Fecha desconocida';
    try {
        return new Date(dateString).toLocaleDateString('es-ES');
    } catch (error) {
        return 'Fecha inválida';
    }
}

function showThreadsLoading() {
    threadsLoading.style.display = 'block';
    threadsList.style.display = 'none';
}

function hideThreadsLoading() {
    threadsLoading.style.display = 'none';
    threadsList.style.display = 'block';
}

function showThreadsError(message) {
    threadsError.textContent = message;
    threadsError.style.display = 'block';
}

function hideThreadsError() {
    threadsError.style.display = 'none';
}

function showError(message) {
    boardHeader.innerHTML = `<div class="error">${message}</div>`;
}

// Hacer funciones globales
window.viewThread = viewThread;
window.goBack = goBack;
window.loadThreads = loadThreads;