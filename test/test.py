# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import numpy as np

N_cycles = 100

@cocotb.test()
async def test_adder(dut):
  dut._log.info("Start")
  
  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  # Set the input values, wait one clock cycle, and check the output
  dut._log.info("Test")
  dut.ui_in.value = 1 # enable randomizer

  R_true = make_randomizer(N_cycles)

  k = 0
  while k < N_cycles:
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == R_true[k]

def make_randomizer(N = 133440):
    '''
    This function creates the PHY pseudo randomization sequence. We use the suggested implementation from CCSDS figure C-1, meaning we assume scambling code number n=0

    Input:
        N = number of symbols to randomize
    '''
    K = 18 #number of bits in register

    x = np.zeros((K,)) # initial generator sequence
    x[0] = 1
    y = np.ones((K,))
    Rn =  np.ones((N,))
    # generate random sequence
    for i in range(N):

        z       = np.mod(x[0] + y[0], 2) # gold sequence
        z1      = np.mod(x[4]+x[6]+x[15], 2) # gold sequence
        z2      = np.mod(y[5] + y[6] + y[8] + y[9] + y[10] + y[11] + y[12] + y[13] + y[14] + y[15], 2)

        z12     = np.mod(z1+z2, 2)
        Rn[i]   = np.mod(2*z12 + z, 4) # mod 4 because we use a 4-bit adder R in 0,1,2,3

        xt   = np.mod(x[7] + x[0], 2)
        yt   = np.mod(y[10]+y[7]+y[5]+y[0], 2)

        x = np.append(x[1:],xt)
        y = np.append(y[1:],yt)
    
    return Rn
