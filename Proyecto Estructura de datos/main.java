import java.util.*;

public class main {
    public static void main(String[] args)
    {
    Scanner scanner = new Scanner (System.in);
    String salir = "";
    
    while (!salir.equals("exit")) 
        //INGRESO DEL USUARIO
        {
        System.out.println("Ingrese nombre:");
        int monto = 1000;
        String nombre = scanner.next();
        System.out.println("Ingrese contraseña:");
        String contraseña = scanner.next();
        System.out.println("Confirme contraseña:");
        String confirmar = scanner.next();
        while (!contraseña.equals(confirmar)) 
            {
            System.out.println("Error: Contraeña incorrecta");
            confirmar = scanner.next();
            }
        //INTERFAZ DE ENTRADA

        System.out.println("Bienvenido " + nombre + " al simulador de inversiones");
        System.out.println("Monto actual -> " + monto + "$");
        while (!salir.equals("enter") && !salir.equals("exit")) 
        {
        System.out.println("");
        System.out.println("Ingresar: enter");
        System.out.println("Salir: exit");
        salir = scanner.next();
        }
        while (!salir.equals("exit")) 
            {
            //CREACIÓN DEL VECTOR GENERADOR DE NUMEROS ALEATORIOS
            int [] numerosApuesta = new int[100];
            int a = 0;
            for (int i = 1; i <= 100; i++)
                {   
                numerosApuesta[a] = i;
                a++;
                }
            Random aleatorio = new Random();
            int indice = aleatorio.nextInt(numerosApuesta.length);
            int valorElegido = numerosApuesta[indice];
            System.out.println("PRIMER VALOR: " + valorElegido);
            System.out.println("¿Cuánto desea ingresar?");
            int montoTemp = scanner.nextInt();
            while (montoTemp > monto) 
                {
                System.out.println("Error: Ingrese un valor menor o igual al monto total");
                montoTemp = scanner.nextInt();
                }
            monto = monto - montoTemp;
            System.out.println("¿El siguiente numero será mayor o menor?");
            System.out.println("Salir: exit");
            salir = scanner.next();
            }
        
        }

    }
    
}
