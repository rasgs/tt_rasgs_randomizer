
`default_nettype	none


// see Appendix C in https://public.ccsds.org/Pubs/131x2b1e1.pdf

module randomizer (
  output wire [1:0] o_r,
  input wire i_clk,
  input wire i_reset,
  input wire i_en
  );

  reg [17:0] x;
  reg [17:0] y;

  initial x = 18'b000000000000000001;
  initial y = 18'b111111111111111111;
  
  wire z1,z2;
  wire z12;
  assign z1= x[4] ^ x[6] ^ x[15];
  assign z2 = y[5] ^ y[6] ^ y[8] ^ y[9] ^ y[10] ^ y[11] ^ y[12] ^ y[13] ^ y[14] ^ y[15];

  assign z12 = z1 ^ z2; // zn(i+131072 mod(2 18-1)) * 2
  assign o_r = {z12, x[0] ^ y[0]};

  always @(posedge i_reset, posedge i_clk) begin
    if (i_reset)
        begin
          x <= 18'b000000000000000001;
          y <= 18'b111111111111111111;
        end
    else if(i_en == 1)
      begin
        x <= { x[7] ^ x[0], x[17:1]};
        y <= { y[10] ^ y[7] ^ y[5] ^ y[0], y[17:1]};
      end
  end

endmodule
