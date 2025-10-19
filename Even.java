import java.util.Scanner;
public class Even
{
public static void main(String[] args)
{
Scanner n1=new Scanner(System.in);
System.out.println("Enter a number: ");
int n=n1.nextInt();
if(n%2==0)
{
System.out.println(n+"Is Even");
}
else
{
System.out.println(n+"Is Odd");
}
}
}