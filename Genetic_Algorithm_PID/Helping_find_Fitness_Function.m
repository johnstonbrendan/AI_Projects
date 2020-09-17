%% Finding ranges of the output values of Q2 function
clear;

K_p_vals = 2:0.5:18;
T_t_vals = 1.05:0.4:9.45;
T_d_vals = 0.26:0.1:2.37;

iterations = length(K_p_vals)*length(T_t_vals)*length(T_d_vals)

x = [0;0;0];
ISE_list = [];
t_r_list = [];
t_s_list = [];
M_p_list = [];

for i = 1:length(K_p_vals)
    x(1,1) = K_p_vals(i);
    for j = 1:length(T_t_vals)
        x(2,1) = T_t_vals(j);
        for k = 1:length(T_d_vals)
            x(3,1) = T_d_vals(k);
            [ISE,t_r,t_s,M_p] = Q2_perfFCN(x);
            ISE_list = [ISE_list;ISE];
            t_r_list = [t_r_list,t_r];
            t_s_list = [t_s_list,t_s];
            M_p_list = [M_p_list,M_p];
        end
    end
end

