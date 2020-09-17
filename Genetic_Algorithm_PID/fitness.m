function [fitness_val] = fitness(x)
%FITNESS Evaluates the fitness of a solution
%   Evaluates the fitness of a given solution. Calls the Q2_perfFCN in
%   order to do the evaluating of the PID parameters, then evaluates the
%   result.
%   Below is what the input (x) values should correspond to:
% Kp = x(1);
% Ti = x(2);
% Td = x(3);

z =  Q2_perfFCN(x);

ISE = z(1)
t_r = z(2)
t_s = z(3)
M_p = z(4)

ISE_prop = 0.2; % these proportions should add up to 1.0
t_r_prop = 0.3;
t_s_prop = 0.3;
M_p_prop = 0.2;

ISE_scale = 0.0199;
t_r_scale = 2.4774;
t_s_scale = 0.0740;
M_p_scale = 0.0184;

fitness_val =   ISE*ISE_scale*ISE_prop + ...
                t_r*t_r_scale*t_r_prop + ...
                t_s*t_s_scale*t_s_prop + ...
                M_p*M_p_scale*M_p_prop;
            
if isnan(fitness_val)
    fitness_val = Inf;
end
end

