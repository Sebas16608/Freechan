console.log('✅ thread.js cargado');

// Configuración
const API_BASE_URL = 'http://localhost:1900';

// Obtener ID del thread de la URL
const urlParams = new URLSearchParams(window.location.search);
const threadId = urlParams.get('id');

console.log('Thread ID from URL:', threadId);

// Elementos del DOM
const threadHeader = document.getElementById('thread-header');
const postsList = document.getElementById('posts-list');
const postsLoading = document.getElementById('posts-loading');
const postsError = document.getElementById('posts-error');
const createPostForm = document.getElementById('create-post-form');

// Inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Iniciando página de thread');
    
    if (!threadId) {
        showError('No se especificó el thread en la URL');
        return;
    }
    
    loadThread();
    loadPosts();
    
    if (createPostForm) {
        createPostForm.addEventListener('submit', handleCreatePost);
    }
});

// Cargar datos del thread
async function loadThread() {
    try {
        console.log('📋 Cargando thread con ID:', threadId);
        const response = await fetch(`${API_BASE_URL}/api/threads/${threadId}`);
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const thread = await response.json();
        console.log('✅ Thread recibido:', thread);
        displayThreadHeader(thread);
        
    } catch (error) {
        console.error('❌ Error cargando thread:', error);
        showError('Error cargando thread: ' + error.message);
    }
}

// Mostrar información del thread
function displayThreadHeader(thread) {
    threadHeader.innerHTML = `
        <div class="thread-main">
            <h2 class="thread-title">${thread.titulo || 'Sin título'}</h2>
            <div class="thread-meta">
                📅 ${formatDate(thread.created)} | 
                ⭐ ${thread.featured ? 'Destacado' : 'Normal'}
            </div>
            <div class="thread-content">
                ${thread.contenido || 'Sin contenido'}
            </div>
        </div>
    `;
}

// Cargar posts del thread
async function loadPosts() {
    showPostsLoading();
    hidePostsError();
    
    try {
        console.log('💬 Cargando posts...');
        const response = await fetch(`${API_BASE_URL}/api/posts`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const allPosts = await response.json();
        console.log('📦 Todos los posts:', allPosts);
        
        // Filtrar posts por thread_id
        const threadPosts = allPosts.filter(post => 
            post.thread_id && parseInt(post.thread_id) === parseInt(threadId)
        );
        
        console.log('✅ Posts del thread:', threadPosts);
        displayPosts(threadPosts);
        
    } catch (error) {
        console.error('❌ Error cargando posts:', error);
        showPostsError('Error cargando posts: ' + error.message);
    } finally {
        hidePostsLoading();
    }
}

// Mostrar posts
function displayPosts(posts) {
    console.log('🎨 Mostrando', posts.length, 'posts');
    
    if (posts.length === 0) {
        postsList.innerHTML = `
            <div class="no-posts">
                <p>💭 No hay respuestas en este thread</p>
                <p><small>Sé el primero en responder!</small></p>
            </div>
        `;
        return;
    }
    
    postsList.innerHTML = posts.map(post => `
        <div class="post-item">
            <div class="post-header">
                <span class="post-author">Anónimo</span>
                <span class="post-date">${formatDate(post.created)}</span>
            </div>
            <div class="post-content">
                ${post.contenido || 'Sin contenido'}
            </div>
            <div class="post-footer">
                <span class="post-stats">#${post.id}</span>
                <div class="post-actions">
                    <button class="post-action" onclick="likePost(${post.id})">👍 Like</button>
                    <button class="post-action" onclick="replyToPost(${post.id})">↩️ Responder</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Crear nuevo post
async function handleCreatePost(event) {
    event.preventDefault();
    
    const content = document.getElementById('post-content').value;
    
    if (!content) {
        alert('Por favor escribe una respuesta');
        return;
    }
    
    try {
        console.log('➕ Creando post...');
        
        const response = await fetch(`${API_BASE_URL}/api/posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contenido: content,
                thread_id: parseInt(threadId),
                featured: false
            })
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('✅ Post creado:', result);
        
        alert('Respuesta publicada!');
        document.getElementById('create-post-form').reset();
        loadPosts();
        
    } catch (error) {
        console.error('❌ Error publicando respuesta:', error);
        alert('Error publicando respuesta: ' + error.message);
    }
}

// Funciones de interacción
function likePost(postId) {
    alert(`Like al post ${postId} (pendiente de implementar)`);
}

function replyToPost(postId) {
    const content = document.getElementById('post-content');
    content.value = `>>${postId}\n`;
    content.focus();
}

// Navegación
function goBack() {
    window.history.back();
}

// Utilidades
function formatDate(dateString) {
    if (!dateString) return 'Fecha desconocida';
    try {
        return new Date(dateString).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return 'Fecha inválida';
    }
}

function showPostsLoading() {
    postsLoading.style.display = 'block';
    postsList.style.display = 'none';
}

function hidePostsLoading() {
    postsLoading.style.display = 'none';
    postsList.style.display = 'block';
}

function showPostsError(message) {
    postsError.textContent = message;
    postsError.style.display = 'block';
}

function hidePostsError() {
    postsError.style.display = 'none';
}

function showError(message) {
    threadHeader.innerHTML = `<div class="error">${message}</div>`;
}

// Hacer funciones globales
window.likePost = likePost;
window.replyToPost = replyToPost;
window.goBack = goBack;
window.loadPosts = loadPosts;