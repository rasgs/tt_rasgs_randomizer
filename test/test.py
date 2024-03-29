# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_adder(dut):
  dut._log.info("Start")

  N_cycles = 100

  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await RisingEdge(dut.clk)
  await RisingEdge(dut.clk)
  await RisingEdge(dut.clk)
  dut.rst_n.value = 1

  # Set the input values, wait one clock cycle, and check the output
  dut._log.info("Test")
  dut.ui_in.value = 1 # enable randomizer

  R_true = make_randomizer(N_cycles)
  print(R_true)
  k = 0
  while k < N_cycles:
    await RisingEdge(dut.clk)
    assert dut.uo_out.value.integer == int(R_true[k])
    k += 1

def make_randomizer(N = 133440):
    '''
    This function creates the PHY pseudo randomization sequence. We use the suggested implementation from CCSDS figure C-1, meaning we assume scambling code number n=0

    Input:
        N = number of symbols to randomize
    '''
    K = 18 #number of bits in register

    x = [0]*K # initial generator sequence
    x[0] = 1
    y = [1]*K
    Rn = [1]*N
    # generate random sequence
    for i in range(N):

        z       = (x[0] + y[0]) % 2 # gold sequence
        z1      = (x[4]+x[6]+x[15]) % 2 # gold sequence
        z2      = (y[5] + y[6] + y[8] + y[9] + y[10] + y[11] + y[12] + y[13] + y[14] + y[15]) % 2

        z12     = (z1+z2) % 2
        Rn[i]   = (2*z12 + z) % 4 # mod 4 because we use a 4-bit adder R in 0,1,2,3

        xt   = (x[7] + x[0]) % 2
        yt   = (y[10]+y[7]+y[5]+y[0]) % 2

        x.append(xt)
        x.pop(0)
        y.append(yt)
        y.pop(0)
    
    return Rn
