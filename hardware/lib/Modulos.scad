
// ===== MÓDULOS COMUNES =====


module rectangulo_vacio_bordes_redondeados(ancho, profundidad, altura, grosor, diametro, alt_c)
{
    //translate([diametro/2, diametro/2, 0])
        difference()
        {
            minkowski()
            {
                cube([ancho-diametro, profundidad-diametro, altura-alt_c], center = true);
                cylinder(d=diametro, h=alt_c, center = false);
                
            }
            //translate([1,1,0])
            //scale([1-Grosor/Ancho,1-Grosor/Ancho,1])
            resize([ancho-grosor*2, profundidad-grosor*2,altura*2])
            minkowski()
            {
                cube([ancho-diametro, profundidad-diametro, altura], center = true);
                cylinder(d=diametro, h=alt_c, $fn=100, center = false);
                
            }
            
        }
    
}


module rectangulo_vacio(ancho, profundidad, altura, grosor)
{
    difference() {
            cube([ancho, profundidad, altura], center=true);
            cube([ancho-2*grosor, profundidad-2*grosor, altura+0.2], center=true);
        }
    
}


module mirror_copy ( v = [1,0,0]){
    children();
    mirror(v) children();
}


module soporte_raspi()

{

include <Medidas.scad>;  
    
    difference()
    {
        cylinder(h=r_sopraspi_altura, d=r_sopraspi_diametro, $fn=200);
        translate([0,0,r_sopraspi_altura*-0.2])
        cylinder(h=r_sopraspi_altura*2, d=r_sopraspi_hueco, $fn=200);
    }
}


module soportes_raspi()
{

include <Medidas.scad>;   
    
    translate([r_dist_tornillo, r_dist_tornillo, 0])
    soporte_raspi();
    translate([r_dist_larg_center_tornillo+r_dist_tornillo, r_dist_anch_center_tornillo+r_dist_tornillo, 0])
    soporte_raspi();
    translate([r_dist_larg_center_tornillo+r_dist_tornillo, r_dist_tornillo, 0])
    soporte_raspi();
    translate([r_dist_tornillo, r_dist_anch_center_tornillo+r_dist_tornillo, 0])
    soporte_raspi();

}
module raspi()
{
    
include <Medidas.scad>;



difference(){

cube([r_largo, r_ancho, r_grosor]);
    translate([r_dist_tornillo, r_dist_tornillo, -10])
    cylinder(h=20, d = r_diametro_interior_tornillo, $fn=200);
    translate([r_largo-r_dist_tornillo, r_ancho-r_dist_tornillo, -10])
    cylinder(h=20, d = r_diametro_interior_tornillo, $fn=200);
    translate([r_largo-dist_tornillo, r_dist_tornillo, -10])
    cylinder(h=20, d = r_diametro_interior_tornillo, $fn=200);
    translate([r_dist_tornillo, r_ancho - r_dist_tornillo, -10])
    cylinder(h=20, d = r_diametro_interior_tornillo, $fn=200);
    
}
    
}

// Prisma trapezoidal: base Y=y, arriba Y=y/2, ancho X=x, alto Z=z
module pulsante_macho(y, x, z, dz=0) {
    // dz te permite alargar un pelín en Z para booleanas (p.ej. dz=0.1)
    pts = [
        // base (z=0)
        [0, 0,   0],   // 0
        [x, 0,   0],   // 1
        [x, y,   0],   // 2
        [0, y,   0],   // 3
        // arriba (z=z+dz)
        [0, 0,   z+dz],   // 4
        [x, 0,   z+dz],   // 5
        [x, y/2, z+dz],   // 6
        [0, y/2, z+dz]    // 7
    ];

    faces = [
        // BASE -> normal hacia -Z (CW visto desde arriba)
        [0,3,2], [0,2,1],
        // ARRIBA -> normal hacia +Z (CCW visto desde arriba)
        [4,5,6], [4,6,7],
        // LATERALES (todas CCW vistas desde fuera)
        [0,1,5], [0,5,4],
        [1,2,6], [1,6,5],
        [2,3,7], [2,7,6],
        [3,0,4], [3,4,7]
    ];

    polyhedron(points=pts, faces=faces, convexity=10);
}

module enganche(en_x, en_y, en_z, Grosor, boton, colour, colour2)

{
    union()
    {
        translate([0,en_y/2,en_z/2])
        color(colour)cube([en_x,en_y,en_z], center = true);
        translate([-boton/2,en_y,en_z-boton*1.5])
        //color(colour2)cube([boton,Grosor*2,boton], center = true);
        rotate([0,tan((Grosor/4)/(boton)),0])
        //linear_extrude(height = boton, scale = [1, 0.5])  // X se mantiene, Y se reduce a la mitad
         //   color(colour2)square([boton, Grosor], center=true);
        pulsante_macho(Grosor,boton,boton);
     }
}

module enganche_molde(en_x, en_y, en_z, Grosor, boton, colour, colour2)

{
    union()
    {
        translate([0,en_y/2,en_z/2])
        color(colour)cube([en_x,en_y,en_z], center = true);
        translate([-boton/2,en_y,en_z-boton*1.5])
        //color(colour2)cube([boton,Grosor*2,boton], center = true);
        rotate([0,tan((Grosor/4)/(boton)),0])
        //linear_extrude(height = boton, scale = [1, 0.5])  // X se mantiene, Y se reduce a la mitad
         //   color(colour2)square([boton, Grosor], center=true);
        cube([4.2,4.2,4.2]);
     }
}

module oled()



{

union()
    {
        translate([0,4.3,-2.5]){
            cube([27.4, 19,5]);
            translate([7.5,19,0])
                cube([12, 4.3, 5]);
            
            
        }
        translate([8.5,1,-2.5])
        cube([10,2,5]);
    }

translate([2,2,-2.5])    
cylinder(d=2.1,h=5, $fn = 400);
    
translate([25.4,2,-2.5])    
cylinder(d=2.1,h=5, $fn = 400);
    
translate([25.4,27.65-2,-2.5])    
cylinder(d=2.1,h=5, $fn = 400);

translate([2,27.65-2,-2.5])    
cylinder(d=2.1,h=5, $fn = 400);   
}



module tapa(
    T_Largo,
    T_Ancho,
    T_Alto,
    T_Grosor,
    T_BiselY,
    T_BiselZ
){
    
    
    // Perfil 2D (Y-Z) de la tapa exterior con bisel en el frente (y=0)
    module perfil_exterior(ancho, alto, by, bz){
        // Asegura que el bisel no exceda dimensiones
        by = min(by, ancho);
        bz = min(bz, alto);
        polygon(points=[
            [0,0],                // frente, base
            [ancho,0],            // fondo, base
            [ancho,alto],         // fondo, arriba
            [by,alto],            // punto sobre la tapa antes del bisel
            [0,alto-bz]           // frente, punto del bisel
        ]);
    }
    rotate([90,0,270])
    translate([-T_Ancho,0,-T_Largo])
    // Cuerpo exterior
        
    difference()
    {//este sirve para hacer los huecos finales a los laterales
        
        union(){
            difference(){
            // Extruimos el perfil exterior a lo largo del largo
                linear_extrude(height=T_Largo)
                    perfil_exterior(T_Ancho,T_Alto,T_BiselY,T_BiselZ);

            // Cavidad interior (deja paredes en todo el contorno y la tapa)
                translate([T_Grosor,0,0])                 // deja grosor en la cara frontal
                    linear_extrude(height=T_Largo-1*T_Grosor)   // y en la cara trasera
                        offset(delta=-T_Grosor)
                            perfil_exterior(T_Ancho,T_Alto,T_BiselY,T_BiselZ);
            
            //Base quitamos base
                translate([1*T_Grosor,0,1*T_Grosor])
                cube([T_Ancho-2*T_Grosor, T_Grosor*4, T_Largo-2*T_Grosor]);
        
            //Quitamos OLED
            //X = Creation Z, Y = Creation X,  Z = Creation Y
                translate([T_Ancho*0.9,T_Alto,(2/9)*T_Largo]) 
                rotate([0,90,90])
            
                oled();
            //Quitamos 2 seguidos    
                translate([T_Ancho*0.9,T_Alto,(7/9)*T_Largo]) 
                rotate([0,90,90])
            
                oled();
                translate([T_Ancho*0.9,T_Alto,(7/9)*T_Largo+27.4]) 
                rotate([0,90,90])
            
                oled();
     
            



        
            }
    
/*
                //Ponemos el fondo
                    translate([T_Ancho-T_Grosor,0,0])
                    cube([T_Grosor, T_Alto, T_Largo]);
    
                //Ponemos el lateral
                    translate([0,0,0])
                    linear_extrude(height=T_Grosor)
                        perfil_exterior(T_Ancho,T_Alto,T_BiselY,T_BiselZ);

 
 */

    
        }
    //X = Creation Z, Y = Creation X,  Z = Creation Y   
    //Quitamos Aberturas 
        
        //Enganche LATERALES
        translate([T_Ancho/2,6,140])
        cube([4.1,4.1,600], center = true);
        
        //Enganche Traseras
        translate([100,6,T_Largo/4])
        color("red")cube([60,4.1,4.1], center = true);  
      
        translate([100,6,T_Largo*(3/4)])
        color("red")cube([60,4.1,4.1], center = true);  

        //Enganche Frontales
        translate([1.2,2,T_Largo/4])
        color("red")cube([1,4.1/2,4.1/2], center = true);  
      
        translate([1.2,2,T_Largo*(3/4)])
        color("red")cube([1,4.1/2,4.1/2], center = true);  


        
            //Abertura RCA Trasera
        translate([100,T_Alto-12,T_Largo*(0.85)])
        rotate([0,90,0])
        color("red")cylinder(h=50,d=10, $fn=200);
        
        translate([100,T_Alto-12,T_Largo*(0.85)-14])
        rotate([0,90,0])
        color("red")cylinder(h=50,d=10, $fn=200);
        
        
             //Abertura RCA Lateral
        translate([88,T_Alto-12,T_Largo*(0.85)])
        rotate([0,0,0])
        color("blue")cylinder(h=50,d=10, $fn=200);
        
        translate([88+14,T_Alto-12,T_Largo*(0.85)])
        rotate([0,0,0])
        color("red")cylinder(h=50,d=10, $fn=200);
        
              //Abertura para botones
        
            
        translate([0,T_Alto*1.3,T_Largo*(1/8)])
        rotate([0,-90,atan(T_BiselZ/T_BiselY)+90])
        color("red")cylinder(h=50,d=16, $fn=200);
        
        
        translate([0,T_Alto*1.3,T_Largo*(3/8)])
        rotate([0,-90,atan(T_BiselZ/T_BiselY)+90])
        color("red")cylinder(h=50,d=16, $fn=200);    
       
        translate([0,T_Alto*1.3,T_Largo*(5/8)])
        rotate([0,-90,atan(T_BiselZ/T_BiselY)+90])
        color("red")cylinder(h=50,d=16, $fn=200);  

        translate([0,T_Alto*1.3,T_Largo*(7/8)])
        rotate([0,-90,atan(T_BiselZ/T_BiselY)+90])
        color("red")cylinder(h=50,d=16, $fn=200);
      
            //pequenos Botones selectores ó volumen
            
        translate([T_Ancho*0.5,T_Alto-2,(6.5/9)*T_Largo]) 
        rotate([0,90,90])
        cube(6);

        translate([T_Ancho*0.5,T_Alto-2,(7.5/9)*T_Largo]) 
        rotate([0,90,90])
        cube(6);
            
        
    }
}



