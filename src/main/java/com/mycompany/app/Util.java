package com.mycompany.app;

/* 
 * This is a utility class
 */
public class Util
{
    public static int add(int num1, int num2) 
    {
    	if (num1 > 0)
    		return num1+num2;	
    	else
    		return num1-num2;
    }

    
    public static int subtract(int num1, int num2) 
    {
        return num1-num2;
    }

    public static int multiply(int num1, int num2) 
    {
        return num1*num2;
    }

    public static int divide(int num1, int num2) 
    {
        return num1/num2;
    }
}
