// Archivo: Looper_bottom.scad
// Incluye las medidas
include <lib/Medidas.scad>;
use <lib/Modulos.scad>

/*

difference()
{
translate([Largo/2, Ancho/2, Alto/2])
color("green")rectangulo_vacio_bordes_redondeados(Largo, Ancho, Alto, Grosor, Diametro, Alt_c);
translate([Largo-6, Ancho-(Ancho/3),0])
cube([12,12,6]);
    
}

*/

difference()
{
    rotate([0,0,90])
    translate([Ancho/2, -Largo/2, Alto/2])
    
    rectangulo_vacio(Ancho,Largo,Alto,Grosor);
    
    translate([Largo-6, Ancho-(Ancho/3),0])
    cube([12,12,6]);
}

