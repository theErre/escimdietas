document.getElementById('antiguedad').style.background = '#12203e';

function myFunction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[4];
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

var horas = []

var table, tr, td, a;
table = document.getElementById('myTable');
tr = table.getElementsByTagName("tr");
for(i=0; i<tr.length; i++){
  td = tr[i].getElementsByTagName("td")[0]
  txtValue = td.textContent || td.innerText;
  if (txtValue.indexOf(".0") > -1){
    tr[i].style.background = "#a1b1ff"
  }
}

