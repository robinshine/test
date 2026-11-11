package com.mycompany.app;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/**
 * Unit test for simple App.
 */
public class UtilTest 
{
    @Test
    public void test()
    {
        assertEquals(2, Util.add(1, 1));
        assertEquals(0, Util.add(-1, -1));
        assertEquals(4, Util.mul(2, 2));
    }
}
