// archivo: boards.js
const resultado = document.getElementById("resultado");

fetch("http://127.0.0.1:8000/boards/api/board/")
  .then(response => {
    if (!response.ok) throw new Error("No se pudo cargar los tableros");
    return response.json();
  })
  .then(data => {
    // data es un array de tableros
    resultado.innerHTML = data.map(board => `
      <div class="tablero">
        <h3>${board.titulo}</h3>
        <p>${board.descripcion}</p>
        <img src="${board.portada}" alt="${board.titulo}" />
        <small>Creado: ${new Date(board.create_at).toLocaleString()}</small>
      </div>
    `).join("");
  })
  .catch(error => {
    resultado.innerText = "Error: " + error.message;
  });
