var table, tr, td, a;
table = document.getElementById('myTable');
tr = table.getElementsByTagName("tr");
for(i=0; i<tr.length; i++){
  td = tr[i].getElementsByTagName("td")[0]
  txtValue = td.textContent || td.innerText;  
  if (txtValue.indexOf(".0") > -1){
    tr[i].style.background = "#a1b1ff"
    tr[i].onclick = ''
  }
}

function OpenModal() {
  let element = document.getElementById('overlay')
  element.style.display = 'block'
}
function CloseModal() {
  let element = document.getElementById('overlay')
  element.style.display = 'none'
}