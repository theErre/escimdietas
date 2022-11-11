legajo = document.getElementById('legajo').value
const header_perfil = document.getElementById('header_perfil')
header_perfil.insertAdjacentHTML('beforeend', '<div class="boton"><a href="/perfil/' + legajo + '/documentosDigitalizados" id="doc_digitalizados">Documentos Digitalizados</a></div>')


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