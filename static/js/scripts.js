$(document).ready(function () {
    function filterTable() {
      var idValue = normalizeString($("#filterID").val());
      var nameValue = normalizeString($("#filterName").val());
      var companyValue = normalizeString($("#filterCompany").val());
      var locationValue = normalizeString($("#filterLocation").val());

      $("#myTable tbody tr").filter(function () {
        $(this).toggle(
          normalizeString($(this).find("td:nth-child(2)").text()).indexOf(idValue) > -1 &&
          normalizeString($(this).find("td:nth-child(3)").text()).indexOf(nameValue) > -1 &&
          normalizeString($(this).find("td:nth-child(4)").text()).indexOf(companyValue) > -1 &&
          normalizeString($(this).find("td:nth-child(5)").text()).indexOf(locationValue) > -1
        );
      });

      // Atualizar contagem de resultados
      var count = $("#myTable tbody tr:visible").length; // Contar apenas linhas visíveis no tbody
      $("#resultCount").text("Resultados encontrados: " + count);
    }

    function normalizeString(str) {
      return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }

    // Filtro por todos os campos
    $("input[type='text']").on("keyup", filterTable);

    // Inicializar a contagem com o total de resultados
    filterTable();

    // Get the modals
    var addModal = document.getElementById("addModal");
    var editModal = document.getElementById("editModal");

    // Get the buttons that open the modals
    var addBtn = document.getElementById("addNewRecordBtn");

    // Get the <span> elements that close the modals
    var addSpan = document.getElementById("addClose");
    var editSpan = document.getElementById("editClose");

    // Open the add modal
    addBtn.onclick = function () {
      addModal.style.display = "block";
    }

    // Open the edit modal
    window.openEditModal = function (id, name, company, location) {
      $("#editID").val(id);
      $("#editName").val(name);
      $("#editCompany").val(company);
      $("#editLocation").val(location);
      editModal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modals
    addSpan.onclick = function () {
      addModal.style.display = "none";
    }

    editSpan.onclick = function () {
      editModal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modals, close them
    window.onclick = function (event) {
      if (event.target == addModal) {
        addModal.style.display = "none";
      }
      if (event.target == editModal) {
        editModal.style.display = "none";
      }
    }
  });


  // Exemplo de função para abrir o modal e preencher os campos
function openEditModal(id, name, company, location) {
  document.getElementById('editID').value = id;
  document.getElementById('editName').value = name;
  document.getElementById('editCompany').value = company;
  document.getElementById('editLocation').value = location;
  document.getElementById('modalEditName').innerText = name;

  // Exibe o modal
  var modal = document.getElementById('editModal');
  modal.style.display = "block";
}

// Fechar o modal ao clicar no "X"
document.getElementById('editClose').onclick = function() {
  document.getElementById('editModal').style.display = "none";
}

// Exemplo de como chamar a função, com valores de exemplo
// openEditModal(1, 'Ana Souza', 'TechSolutions', 'São Paulo');
