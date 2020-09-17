function z = Q2_perfFCN(x)

Kp = x(1);
Ti = x(2);
Td = x(3);
G = Kp*tf([Ti*Td,Ti,1],[Ti,0]);

F = tf(1,[1,6,11,6,0]);
sys = feedback(series(G,F),1);
sysinf = stepinfo(sys);
t = 0:0.01:100;
y = step(sys,t);

ISE = sum((y-1).^2);
t_r = sysinf.RiseTime;
t_s = sysinf.SettlingTime;
M_p = sysinf.Overshoot;

z(1) = ISE;
z(2) = t_r;
z(3) = t_s;
z(4) = M_p;
end