document.getElementById('infoPersonal').style.background = '#13203e';
legajo = document.getElementById('legajo').value
const header_perfil = document.getElementById('header_perfil')
header_perfil.insertAdjacentHTML('beforeend', '<div class="boton"><a href="/perfil/' + legajo + '/documentosDigitalizados" id="doc_digitalizados">Documentos Digitalizados</a></div>')

var elementos = document.getElementsByTagName("input");

for (i = 0; i < elementos.length; i++) {
  if (elementos[i].type != "file") {
    elementos[i].disabled = true;
  }
}


var grado = ["MP", "CS", "CP", "SOS", "SOP", "SOC"]

for (let i = 0; i < grado.length; i++) {
  if (elementos[13].value == 'MP') {
    elementos[13].value = 'Marinero de Primera';
    break
  } else if (elementos[13].value == 'CS') {
    elementos[13].value = 'Cabo de Segunda';
    break
  } else if (elementos[13].value == 'CP') {
    elementos[13].value = 'Cabo de Primera';
    break
  } else if (elementos[13].value == 'SOS') {
    elementos[13].value = 'Sub Oficial de Segunda';
    break
  } else if (elementos[13].value == 'SOP') {
    elementos[13].value = 'Sub Oficial de Primera';
    break
  } else if (elementos[13].value == 'SOC') {
    elementos[13].value = 'Sub Oficial de Cargo';
    break
  }
}


function isValidDate(day, month, year) {
  var dteDate;
  month = month - 1;
  dteDate = new Date(year, month, day);
  return ((day == dteDate.getDate()) && (month == dteDate.getMonth()) && (year == dteDate.getFullYear()));
}

function validate_fecha(fecha) {
  var patron = new RegExp("^(19|20)+([0-9]{2})([-])([0-9]{1,2})([-])([0-9]{1,2})$");
  if (fecha.search(patron) == 0) {
    var values = fecha.split("-");
    if (isValidDate(values[2], values[1], values[0])) {
      return true;
    }
  }
  return false;
}

function calcularTiempo(dato) {
  var fecha = dato
  if (validate_fecha(fecha) == true) {
    var values = fecha.split("-");
    var dia = values[2];
    var mes = values[1];
    var ano = values[0];
    var fecha_hoy = new Date();
    var ahora_ano = fecha_hoy.getYear();
    var ahora_mes = fecha_hoy.getMonth() + 1;
    var ahora_dia = fecha_hoy.getDate();
    var edad = (ahora_ano + 1900) - ano;
    if (ahora_mes < mes) {
      edad--;
    }
    if ((mes == ahora_mes) && (ahora_dia < dia)) {
      edad--;
    }
    if (edad > 1900) {
      edad -= 1900;
    }

    var meses = 0;

    if (ahora_mes > mes)
      meses = ahora_mes - mes;

    if (ahora_mes < mes)
      meses = 12 - (mes - ahora_mes);

    if (ahora_mes == mes && dia > ahora_dia)
      meses = 11;

    return [edad, meses];
  }
}

var fecha_nacimiento = document.getElementById('fecha_nacimiento').value;
var resultado = calcularTiempo(fecha_nacimiento);
document.getElementById('edad').value = resultado[0] + " Años";

var fecha_ingreso = document.getElementById('fecha_ingreso').value;
var resultado = calcularTiempo(fecha_ingreso);
document.getElementById('antiguedadArmada').value = resultado[0] + " Años y " + resultado[1] + " Meses"


// Obtener referencia al input y a la imagen

const $seleccionArchivos = document.querySelector("#seleccionArchivos"),
  $imagenPrevisualizacion = document.querySelector("#imagenPrevisualizacion");

// Escuchar cuando cambie
$seleccionArchivos.addEventListener("change", () => {
  // Los archivos seleccionados, pueden ser muchos o uno
  const archivos = $seleccionArchivos.files;
  // Si no hay archivos salimos de la función y quitamos la imagen
  if (!archivos || !archivos.length) {
    $imagenPrevisualizacion.src = "";
    return;
  }
  // Ahora tomamos el primer archivo, el cual vamos a previsualizar
  const primerArchivo = archivos[0];
  // Lo convertimos a un objeto de tipo objectURL
  const objectURL = URL.createObjectURL(primerArchivo);
  // Y a la fuente de la imagen le ponemos el objectURL
  $imagenPrevisualizacion.src = objectURL;
});