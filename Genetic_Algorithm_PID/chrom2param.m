function [x] = chrom2param(chrom)
%CHROM2PARAM Converts chromozone to repsective PID param values
%   Detailed explanation goes here

chrom = char(chrom);
K_p_c = chrom(1:11);
T_t_c = chrom(12:21);
T_d_c = chrom(22:29);

K_p = bin2dec(K_p_c);
T_t = bin2dec(T_t_c);
T_d = bin2dec(T_d_c);

K_p = K_p / 100;
T_t = T_t / 100;
T_d = T_d / 100;

K_p = K_p + 2;
T_t = T_t + 1.05;
T_d = T_d + 0.26;

x(1) = K_p;
x(2) = T_t;
x(3) = T_d;

end

