<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
This code is based on the CCSDS 131.2-B-2 standard, for high-rate telemetry sattelite communications: https://public.ccsds.org/Pubs/131x2b2.pdf 

This code generates a pseudo-random number between 0 and 3, which is used for performing the physical layer IQ pseudo-randomization.
The code is based on the randomizer described in Annex C of CCSDS 131.2-B-2. 

## How to test

Run the cocotb testbench and compare it to the randomizer specified in Python, using the 'make_randomizer' function.

## External hardware

No external HW needed for now. However, the output of the module can be used for an AXI-based scrambler of the I and Q complex baseband signals. 
This could e.g. be done like this:

```
always @(posedge i_clk) begin
  case(r)
  2'b00:
    begin
      o_I = in_I;
      o_Q = in_Q;
    end
  2'b01:
    begin
      o_I = -in_Q;
      o_Q = in_I;
    end
  2'b10:
    begin
      o_I = -in_I;
      o_Q = -in_Q;
    end
  2'b11:
    begin
      o_I = in_Q;
      o_Q = -in_I;
    end
  endcase
end
```
