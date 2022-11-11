document.getElementById('cursosPostula').style.background = '#12203e';
document.getElementById('back').href = 'listadoCursosPostula'


function myFunction_materias() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

listado = document.getElementById('listado')


document.getElementById('select').onclick = function () {
  var checkboxes = document.getElementsByName('materias');
  for (var checkbox of checkboxes) {
    if (checkbox.checked) {
      listado.append(checkbox.value + ' ');
    }
  }
}
