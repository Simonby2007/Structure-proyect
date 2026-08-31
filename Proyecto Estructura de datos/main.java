import java.util.*;

public class main {
    public static void main(String[] args)
    {
    Scanner scanner = new Scanner (System.in);
    boolean salir = false;
    String ingreso = "";
    while (!salir) 
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
        while (!salir && !ingreso.equals("enter")) 
        {
        System.out.println("");
        System.out.println("Ingresar: enter");
        System.out.println("Salir: exit");
        ingreso = scanner.next();
        if (ingreso.equals("exit")) 
            {
                salir = true;
                System.out.println("Gracias por usar el simulador de inversiones");
            }
            else if (ingreso.equals("enter")) 
            {

            }else 
            {
                System.out.println("Error: Ingrese un valor valido");
            }
        }
        while (!salir) 
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
                int ValorElegido = numerosApuesta[indice];
                System.out.println("PRIMER VALOR: " + ValorElegido);
                System.out.println("¿Cuánto desea ingresar?");
                int montoTemp = scanner.nextInt();
                while (montoTemp > monto) 
                    {
                    System.out.println("Error: Ingrese un valor menor o igual al monto total");
                    montoTemp = scanner.nextInt();
                    }
                monto = monto - montoTemp;
                //EMPEZAR ALGORITMO DE COMPARACIÓN
                while (!salir)
                {
                    int indice2 = aleatorio.nextInt(numerosApuesta.length);
                    int ValorElegido2 = numerosApuesta[indice2];
                    System.out.println("¿El siguiente numero será:");
                    System.out.println("MAYOR: 1.)");
                    System.out.println("MENOR: 2.)");
                    System.out.println("Ingresar nuevo valor para apostar: 3.)");
                    System.out.println("salir: exit");
                    String comparacion = scanner.next();
                    switch (comparacion) 
                    {
                        case "1":
                            indice2 = aleatorio.nextInt(numerosApuesta.length);
                            ValorElegido2 = numerosApuesta[indice2];
                            System.out.println("SEGUNDO VALOR: " + ValorElegido2);
                            if (ValorElegido2 > ValorElegido)
                            {
                                monto = monto + montoTemp;
                                System.out.println("Ganaste! Monto actual -> " + monto + "$");
                                ValorElegido = ValorElegido2;
                            }
                            else
                            {
                                System.out.println("Perdiste! Monto actual -> " + monto + "$");
                                if (monto == 0)
                                {
                                    System.out.println("No tienes dinero para seguir jugando");
                                    salir = true;
                                }
                            }
                            ValorElegido = ValorElegido2;
                            break;
                        case "2":
                            indice2 = aleatorio.nextInt(numerosApuesta.length);
                            ValorElegido2 = numerosApuesta[indice2];
                            System.out.println("SEGUNDO VALOR: " + ValorElegido2);
                            if (ValorElegido2 < ValorElegido)
                            {
                                montoTemp = montoTemp * 2;
                                monto = monto + montoTemp;
                                System.out.println("Ganaste! Monto actual -> " + monto + "$");
                                ValorElegido = ValorElegido2;
                            }else
                            {
                                System.out.println("Perdiste! Monto actual -> " + monto + "$");
                                if (monto == 0)
                                {
                                    System.out.println("No tienes dinero para seguir jugando");
                                    salir = true;
                                }
                            }
                            ValorElegido = ValorElegido2;
                            break;
                        case "3":
                            monto = monto + montoTemp;
                            System.out.println("Ingrese nuevo valor para apostar:");
                            montoTemp = scanner.nextInt();
                            while (montoTemp > monto) 
                                {
                                System.out.println("Error: Ingrese un valor menor o igual al monto total");
                                montoTemp = scanner.nextInt();
                                }
                            monto = monto - montoTemp;
                            break;
                        case "exit":
                            salir = true;
                            System.out.println("Gracias por usar el simulador de inversiones");
                            break;
                        default:
                            System.out.println("Error: Ingrese un valor valido");
                            break;
                    }
                }
            
            }
        }
        scanner.close();
    }
}

