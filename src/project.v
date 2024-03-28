/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`define default_netname none

module tt_um_rgs_randomizer (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_out[7:0] = 8'b0000_0000;
  assign uio_oe[7:0]  = 8'b0000_0000;

  wire [1:0] o_r;
  wire i_clk, i_reset, i_en;

  assign i_clk = clk;
  assign i_reset = ~rst_n;
  assign i_en = ui_in[0];
  assign uo_out[1:0] = o_r;
  assign uo_out[7:2] = 6'b000000;
  
  randomizer randomizer_inst (
    .i_clk(i_clk),
    .i_reset( i_reset),
    .i_en(i_en),
    .o_r(o_r)
  );

endmodule
