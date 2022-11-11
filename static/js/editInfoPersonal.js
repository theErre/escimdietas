document.getElementById('infoPersonal').style.background = '#12203e';
//cambiamos el boton de volver para que vuelva atras
document.getElementById('back').href = 'infoPersonal'

//creamos una lista para cada compañia con sus secciones
var compania1 = new Array("-- Seleccionar --","Puma", "Lince", "Cuartel General");
var compania2 = new Array("-- Seleccionar --", "Danger", "Charrua", "Cuartel General" );
var compania3 = new Array("-- Seleccionar --", "Camaleon", "Yacare", "Cuartel General");
var compania4 = new Array("-- Seleccionar --", "Acrux", "Albatros", "Cuartel General");
var coffee = new Array("-- Seleccionar --", "Peloton de Embarcaciones", "Peloton de Armas", "Peloton de Operaciones Especiales");
var coser = new Array("-- Seleccionar --", "Cuartel General", "Transporte", "Lavanderia", "Peluqueria", "Mayordomia", "Cocina", "Taller", "Artilleria", "Mantenimiento");
var emcomim = new Array("-- Seleccionar --", "Cuartel General de Comandante", "Secretaria del Comandante", "Personal", "Inteligencia", "Operaciones y Planes", "Logistica", "Contaduria", "Comunicacion");
var esim = new Array("-- Seleccionar --", "Cuartel General", "Division Cursos", "Peloton de Reclutas", "Plantel K-9")

//creamos una lista general con todas las secciones 
var todasCompanias = [
  [],
  compania1,
  compania2,
  compania3,
  compania4,
  coffee,
  coser,
  esim,
  emcomim,
];

//funcion que se encargara de conectar los dos seclect options -compañia/seccion-
function selected_seccion(){ 
  let brigada = document.getElementById('compania').selectedIndex;
  let seccion = document.getElementById('seccion')
  if(brigada != 0){
    todas_secciones = todasCompanias[brigada];
    num_secciones = todas_secciones.length;
    seccion.length = num_secciones;
    for(i=0; i<num_secciones; i++){
      seccion.options[i].value = todas_secciones[i];
      seccion.options[i].text = todas_secciones[i];
    }
  } else {
    seccion.length = 1;
    seccion.options[0].value = ""
    seccion.options[0].text = "-- Selecionar una Compañia --"
  }
  seccion.options[0].selected = true
}

//establecemos dos variables que almacenan el grado actual y listado con los grados
var grado_actual = document.getElementById('grado_actual').value;
var grado = document.getElementById('grado');
//funcion que se encargara de recorrer el listado para establecer el grado actual
for(i=0; i<grado.length; i++){
  if(grado.options[i].value == grado_actual){
    grado.options[i].selected = true
    break
  }
}

//recuperamos la compania actual y la seccion actual para mostrarla
var compania_actual = document.getElementById('compania_actual').value;
var seccion_actual = document.getElementById('seccion_actual').value;
//funcion que se encargara de mostrar en la pantalla la compania y la seccion actual
var companias = document.getElementById('compania');
var secciones = document.getElementById('seccion');
for(i=0; i<companias.length; i++){
  if(companias[i].value == compania_actual){
    companias[i].selected = true;
    for(a=0; a<todasCompanias[i].length; a++){
      console.log(todasCompanias[i][a])
      if(todasCompanias[i][a] == seccion_actual){
        secciones[0].value = seccion_actual
        secciones[0].text = seccion_actual
        secciones[0].selected = true
      }
    }
  }
}


function isValidDate(day,month,year){
  var dteDate;
  month=month-1;
  dteDate=new Date(year,month,day);
  return ((day==dteDate.getDate()) && (month==dteDate.getMonth()) && (year==dteDate.getFullYear()));
}

function validate_fecha(fecha){
  var patron=new RegExp("^(19|20)+([0-9]{2})([-])([0-9]{1,2})([-])([0-9]{1,2})$");
  if(fecha.search(patron)==0){
      var values=fecha.split("-");
      if(isValidDate(values[2],values[1],values[0])) {
          return true;
      }
  }
  return false;
}

function calcularTiempo(dato){
  var fecha = dato
  if(validate_fecha(fecha)==true){
    var values=fecha.split("-");
    var dia = values[2];
    var mes = values[1];
    var ano = values[0];
    var fecha_hoy = new Date();
    var ahora_ano = fecha_hoy.getYear();
    var ahora_mes = fecha_hoy.getMonth()+1;
    var ahora_dia = fecha_hoy.getDate();
    var edad = (ahora_ano + 1900) - ano;
    if ( ahora_mes < mes ){
        edad--;
    }
    if ((mes == ahora_mes) && (ahora_dia < dia)){
        edad--;
    }
    if (edad > 1900){
        edad -= 1900;
    }

    var meses=0;

    if(ahora_mes>mes)
        meses=ahora_mes-mes;

    if(ahora_mes<mes)
        meses=12-(mes-ahora_mes);

    if(ahora_mes==mes && dia>ahora_dia)
        meses=11;

    return [edad, meses];
  }
}

var fecha_nacimiento = document.getElementById('fecha_nacimiento').value;
var resultado = calcularTiempo(fecha_nacimiento);
document.getElementById('edad').value = resultado[0] + " Años";

var fecha_ingreso = document.getElementById('fecha_ingreso').value;
var resultado = calcularTiempo(fecha_ingreso);
document.getElementById('antiguedad').value = resultado[0] + " Años y " + resultado[1] + " Meses";