//color de fondo del boton Otros Datos
document.getElementById('otrosDatos').style.background = '#12203e';

//modficamos la direccion para volver a otrosDatos y no volver al inicio
document.getElementById('back').href = 'otrosDatos';

//creamos una variable para poder trabajar con el input radio de Trabajo, Estudio, ssee, Retencion
var trabaja = document.getElementById('trabaja').value;
var estudia = document.getElementById('estudia').value;
var ssee = document.getElementById('ssee').value;
var retencion = document.getElementById('retencion').value;

//Recuperamos el dato de la base, si es si mostramos el contenedor
if(trabaja == 'Si'){
    document.getElementById('trabaja_si').checked = true;
    document.getElementById('trabaja_no').checked = false;
    trabaja_mostrar()
} else {
    document.getElementById('trabaja_si').checked = false;
    document.getElementById('trabaja_no').checked = true;
    trabaja_ocultar()
}

if(estudia == 'Si'){
    document.getElementById('estudia_si').checked = true;
    document.getElementById('estudia_no').checked = false;
    estudio_mostrar()
} else {
    document.getElementById('estudia_si').checked = false;
    document.getElementById('estudia_no').checked = true;
    estudio_ocultar()
}

if(ssee == 'Si'){
    document.getElementById('ssee_si').checked = true;
    document.getElementById('ssee_no').checked = false;
} else {
    document.getElementById('ssee_si').checked = false;
    document.getElementById('ssee_no').checked = true;
}

if(retencion == 'Si'){
    document.getElementById('retencion_si').checked = true;
    document.getElementById('retencion_no').checked = false;
} else {
    document.getElementById('retencion_si').checked = false;
    document.getElementById('retencion_no').checked = true;
}

function trabaja_ocultar(){
    document.getElementById('box-trabajo').style.display = 'none';
    document.getElementById('nombre_empresa').value = "No Trabaja"
    document.getElementById('telefono_empresa').value = "No Trabaja"
    document.getElementById('direccion_empresa').value = "No Trabaja"
}

function trabaja_mostrar(){
    document.getElementById('box-trabajo').style.display = 'inline';
    document.getElementById('nombre_empresa').value = ""
    document.getElementById('telefono_empresa').value = ""
    document.getElementById('direccion_empresa').value = ""
}

function estudio_ocultar(){
    document.getElementById('box-estudio').style.display = 'none';
    document.getElementsByName('lugar_estudio').value = 'No Estudia';
    document.getElementsByName('direccion_estudio').value = 'No estudia';
    document.getElementsByName('horario_estudio').value = 'No Estudia'; 
}

function estudio_mostrar(){
    document.getElementById('box-estudio').style.display = 'inline'
    document.getElementsByName('lugar_estudio').value = '';
    document.getElementsByName('direccion_estudio').value = '';
    document.getElementsByName('horario_estudio').value = '';
}