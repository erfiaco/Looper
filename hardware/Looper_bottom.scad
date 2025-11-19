// Archivo: Looper_bottom.scad
// Incluye las medidas
use<lib/Modulos.scad>
include <lib/Medidas.scad>;


// Cubo base (center = false)
translate([0,0,0])
color("purple")cube([Largo, Ancho, Grosor], center=false);

translate([Largo-80,10,Grosor])
//rotate([0,-180,-90])

soportes_raspi();

import("lib/Looper_middle.stl");

en_x = 6.4;
en_y = 1.4;
en_z = 20;
en_z2 = 14;
en_colour = "green";
en_colour2 = "red";
boton = 4;

//BACK

rotate([0,0,180])
translate([-Largo/4,-Grosor-en_y,0])
enganche(en_x, en_y, en_z, Grosor,boton,"green", "red");

rotate([0,0,180])
translate([-Largo*3/4,-Grosor-en_y,0])
enganche(en_x, en_y, en_z, Grosor,boton,"green", "red");

//FRONT

rotate([0,0,180])
translate([-Largo/4,-T_Ancho+Grosor+en_y,0])
rotate([0,0,180])
enganche(en_x, en_y, en_z2, Grosor/2,boton/2,"green", "red");

rotate([0,0,180])
translate([-Largo*3/4,-T_Ancho+Grosor+en_y,0])
rotate([0,0,180])
enganche(en_x, en_y, en_z2, Grosor/2,boton/2,"green", "red");



//Laterals
rotate([0,0,90])
translate([+Ancho/2,-Grosor-en_y,0])
enganche(en_x, en_y, en_z, Grosor,boton,"green", "red");


translate([Largo-Grosor-en_y,+Ancho/2,0])
rotate([0,0,-90])
enganche(en_x, en_y, en_z, Grosor,boton,"green", "red");