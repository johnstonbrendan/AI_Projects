function [chromo] = param2chrom(x)
%PARAM2CHROM Converts PID parameters to chromosone
%   Detailed explanation goes here

K_p = x(1); % Will need 11 bits
T_t = x(2); % Will need 10 bits
T_d = x(3); % Will need 8 bits

% Subtract the lower range
K_p = K_p - 2; % K_p has range 2-18
T_t = T_t - 1.05; % T_t has range 1.05 - 9.42
T_d = T_d - 0.26; % T_d has range 0.26 - 2.37

% Multiply by 100 for a precision of 2 decimal places
% Round to remove floating point arithmetic
K_p = round(K_p * 100);
T_t = round(T_t * 100);
T_d = round(T_d * 100);


% Convert non-decimal to binary (chromozone components)(_c)
K_p_c = dec2bin(K_p,11);
T_t_c = dec2bin(T_t,10);
T_d_c = dec2bin(T_d,8);

chromo = [K_p_c,T_t_c,T_d_c];


end

