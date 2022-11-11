document.getElementById('infoCursos').style.background = '#12203e'
var legajo = document.getElementById('legajo').value
document.getElementById('back').href = '/perfil/' + legajo + '/infoCursos'

var elems = document.getElementsByClassName('confirmation_cursos');
var confirmIt = function (e) {
    if (!confirm('Desea Eliminar este dato de Cursos?')) e.preventDefault();
};
for (var i = 0, l = elems.length; i < l; i++) {
    elems[i].addEventListener('click', confirmIt, false);
}
