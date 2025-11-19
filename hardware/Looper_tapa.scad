// -----------------------------
// Tapa hueca con bisel superior
// -----------------------------
/*
Parámetros:
- T_Largo   : largo (eje X)
- T_Ancho   : ancho (eje Y)
- T_Alto    : alto   (eje Z)
- T_Grosor  : grosor de pared
- T_BiselY  : cuánto entra el bisel desde el frente (en Y)
- T_BiselZ  : cuánto baja el bisel desde la parte superior (en Z)
   
*/


include <lib/Medidas.scad>;
use <lib/Modulos.scad>;

difference(){
    union(){
        tapa(
            T_Largo,
            T_Ancho,
            T_Alto,
            T_Grosor,
            T_BiselY,
            T_BiselZ
        );
//Largo/2
    /*translate([T_Largo/2,3+0.5*T_Grosor,T_Alto/3])
    rotate([0,-90,0])
    color("red")soporte_raspi();

    translate([T_Largo/2,3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("red")soporte_raspi();
        
    translate([T_Largo/2,T_Ancho/4 + 3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("red")soporte_raspi();
    
    translate([T_Largo/2,2*T_Ancho/4 + 3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("red")soporte_raspi();
    
    translate([T_Largo/2,T_Ancho*0.68 + 3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("red")soporte_raspi();
    
    translate([T_Largo/2,T_Ancho*0.94 + 3+0.5*T_Grosor,T_Alto*0.1])
    rotate([0,-90,0])
    color("red")soporte_raspi();
    
    
    //Largo/2 + 3
    translate([3+T_Largo/2,3+0.5*T_Grosor,T_Alto/3])
    rotate([0,-90,0])
    color("blue")soporte_raspi();

    translate([3+T_Largo/2,3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("blue")soporte_raspi();
        
    translate([3+T_Largo/2,T_Ancho/4 + 3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("blue")soporte_raspi();
    
    translate([3+T_Largo/2,2*T_Ancho/4 + 3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("blue")soporte_raspi();
    
    translate([3+T_Largo/2,T_Ancho*0.68 + 3+0.5*T_Grosor,T_Alto-3-0.5*T_Grosor])
    rotate([0,-90,0])
    color("blue")soporte_raspi();
    
    translate([3+T_Largo/2,T_Ancho*0.94 + 3+0.5*T_Grosor,T_Alto*0.1])
    rotate([0,-90,0])
    color("blue")soporte_raspi();
    */
        

    }
    
    

}