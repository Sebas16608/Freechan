fetch('http://127.0.0.1:8000/boards/api/board/')
  .then(res => res.json())
  .then(data => {
      const lista = document.getElementById('lista-boards');
      data.forEach(board => {
          const li = document.createElement('li');
          li.textContent = board.titulo + " - " + board.contenido;
          lista.appendChild(li);
      });
  });
