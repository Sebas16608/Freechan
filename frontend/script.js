console.log('✅ script.js cargado correctamente');

// Configuración de la API
const API_BASE_URL = 'http://localhost:1900';

// Elementos del DOM
const boardsGrid = document.getElementById('boards-grid');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const featuredThreadsElement = document.getElementById('featured-threads');

// Función para mostrar boards
function displayBoards(boards) {
    console.log('Mostrando boards:', boards);
    
    if (boards.length === 0) {
        boardsGrid.innerHTML = '<div class="no-data">No hay boards disponibles</div>';
        return;
    }
    
    boardsGrid.innerHTML = boards.map(board => `
        <div class="board-card">
            <div class="board-header">
                <span class="board-name">${board.titulo}</span>
                <div>
                    <span class="board-short">${board.short_name}</span>
                    ${board.featured ? '<span class="featured-badge">⭐</span>' : ''}
                </div>
            </div>
            <p class="board-description">${board.descripcion || 'Sin descripción'}</p>
            <div class="board-actions">
                <a href="board.html?id=${board.id}" class="btn btn-primary">
                    🔍 Ver Threads
                </a>
                <a href="board.html?id=${board.id}" class="btn btn-success">
                    ➕ Nuevo Thread
                </a>
            </div>
        </div>
    `).join('');
}

// Función para cargar boards
async function loadBoards() {
    console.log('Cargando boards...');
    loadingElement.style.display = 'block';
    errorElement.style.display = 'none';
    boardsGrid.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/boards`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const boards = await response.json();
        console.log('Boards recibidos:', boards);
        
        displayBoards(boards);
        loadingElement.style.display = 'none';
        boardsGrid.style.display = 'grid';
        
    } catch (error) {
        console.error('Error:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
        errorElement.innerHTML = `
            Error cargando boards: ${error.message}
            <br><br>
            <small>Asegúrate de que:<br>
            1. El servidor Flask esté ejecutándose<br>
            2. La URL sea correcta: ${API_BASE_URL}<br>
            3. No haya problemas de CORS</small>
        `;
    }
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página cargada, iniciando...');
    loadBoards();
});

// Función para probar desde consola
window.testAPI = async function() {
    console.log('Probando API...');
    try {
        const response = await fetch(`${API_BASE_URL}/api/boards`);
        const data = await response.json();
        console.log('✅ API funciona:', data);
        return data;
    } catch (error) {
        console.error('❌ Error API:', error);
        throw error;
    }
};