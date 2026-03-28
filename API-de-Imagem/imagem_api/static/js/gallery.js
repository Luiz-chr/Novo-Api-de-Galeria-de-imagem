const API_URL = "http://127.0.0.1:8000";


async function carregarImagens(query = "") {
  // Se houver busca, usa a rota /search/, senão usa /list/
  const url = query ? `${API_URL}/search/${query}` : `${API_URL}/list/`;
  
  try {
    const res = await fetch(url);
    const data = await res.json();
    
    const gallery = document.getElementById("gallery");
    gallery.innerHTML = ""; // Limpa a galeria antes de recarregar

    if (data.imagens.length === 0) {
      gallery.innerHTML = "<p>Nenhuma imagem encontrada.</p>";
      return;
    }

    data.imagens.forEach(nomeSistema => {
      const container = document.createElement("div");
      container.className = "image-container";

      // A rota de download agora busca pelo nome_sistema (UUID) no MongoDB
      const img = document.createElement("img");
      img.src = `${API_URL}/download/${nomeSistema}`;
      img.alt = "Imagem da Galeria";

      const deleteBtn = document.createElement("button");
      deleteBtn.className = "delete-btn";
      deleteBtn.textContent = "X";
      deleteBtn.onclick = () => deletarImagem(nomeSistema);

      container.appendChild(img);
      container.appendChild(deleteBtn);
      gallery.appendChild(container);
    });
  } catch (error) {
    console.error("Erro ao carregar imagens:", error);
  }
}

// Função para deletar imagem (remove do Disco e do MongoDB)
async function deletarImagem(filename) {
  if (confirm(`Deseja realmente excluir esta imagem?`)) {
    try {
      const res = await fetch(`${API_URL}/delete/${filename}`, { 
        method: "DELETE" 
      });
      if (res.ok) {
        carregarImagens(); // Recarrega a lista após deletar
      }
    } catch (error) {
      alert("Erro ao deletar a imagem.");
    }
  }
}

// Função de busca disparada pelo botão
function buscarImagens() {
  const query = document.getElementById("searchInput").value.trim();
  carregarImagens(query);
}

// Evento de Upload
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files[0]) return;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  
  try {
    const res = await fetch(`${API_URL}/upload/`, {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      fileInput.value = ""; // Limpa o campo de arquivo
      carregarImagens();   // Atualiza a galeria
    } else {
      alert("Erro ao enviar imagem.");
    }
  } catch (error) {
    console.error("Erro no upload:", error);
  }
});

// Inicialização: Carrega as imagens assim que a página abre
carregarImagens();