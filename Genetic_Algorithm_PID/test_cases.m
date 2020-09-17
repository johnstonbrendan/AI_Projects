% Test Cases
%% 1 Default Values
pop = 50;
gens = 150;
cross_prob = 0.6;
mut_prob = 0.25;

[sol_prog_1,best_sol_1] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

%% 2 Changing number of gens
pop = 50;
gens = 75;
cross_prob = 0.6;
mut_prob = 0.25;
[sol_prog_2,best_sol_2] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

gens = 30;
[sol_prog_3,best_sol_3] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

gens = 300;
[sol_prog_4,best_sol_4] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

%% 3 Changing number of population size
pop = 25;
gens = 150;
cross_prob = 0.6;
mut_prob = 0.25;
[sol_prog_5,best_sol_5] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

pop = 10;
[sol_prog_6,best_sol_6] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

pop = 100;
[sol_prog_7,best_sol_7] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

%% 4 Changing Crossover and Mutation Probabilities
pop = 50;
gens = 150;
cross_prob = 0.3; % Halfed crossover probability
mut_prob = 0.125; % Halfed mutation probability
[sol_prog_8,best_sol_8] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.8; % Increased crossover probability
mut_prob = 0.125; % Decreased Mutation probability
[sol_prog_9,best_sol_9] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.3; % Halfed crossover probability
mut_prob = 0.75; % Incrased mutation probability significantly
[sol_prog_10,best_sol_10] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.8; % Increased crossover probability
mut_prob = 0.75; % Incrased mutation probability
[sol_prog_11,best_sol_11] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.8; % Increased crossover probability
mut_prob = 0.25;
[sol_prog_12,best_sol_12] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.3; % Decreased crossover probability
mut_prob = 0.25;
[sol_prog_13,best_sol_13] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.6;
mut_prob = 0.75; % Increased mutation probability
[sol_prog_14,best_sol_14] = genetic_algorithm(gens,pop,cross_prob,mut_prob);

cross_prob = 0.6; 
mut_prob = 0.125; % Decreased mutation probability
[sol_prog_15,best_sol_15] = genetic_algorithm(gens,pop,cross_prob,mut_prob);


%% Plot For Part C
close all;
plot(sol_prog_1);
xlabel('Generation');
ylabel('Fitness');

%% Plot for Part d i
close all;
plot(sol_prog_1);
hold on
plot(sol_prog_2);
xlabel('Generation');
ylabel('Fitness');

plot(sol_prog_3);
plot(sol_prog_4);
legend('Generations = 150','Generations = 50','Generations = 30','Generations = 300');

%% Plot for Part d ii
close all;
plot(sol_prog_1);
xlabel('Generation');
ylabel('Fitness');
hold on;

plot(sol_prog_5);
plot(sol_prog_6);
plot(sol_prog_7);
legend('Population = 50','Population = 25','Population = 10','Population = 100');

%% Plot for d iii
close all;

% Show the ones where crossover is changed
figure();
plot(sol_prog_1);
xlabel('Generation');
ylabel('Fitness');
title('Changing crossover');
hold on;
plot(sol_prog_12);
plot(sol_prog_13);
legend('Crossover = 0.8','Crossover = 0.3','Crossover = 0.6');
hold off;


% Show the ones where mutation is changed
figure();
plot(sol_prog_1);
xlabel('Generation');
ylabel('Fitness');
title('Changing mutation');
hold on;
plot(sol_prog_14);
plot(sol_prog_15);
legend('Mutation = 0.25','Mutation = 0.75','Mutation = 0.125');
hold off;


% Show the ones where both crossover and mutation are changed
figure();
plot(sol_prog_1);
xlabel('Generation');
ylabel('Fitness');
title('Changing crossover and mutation');
hold on;
plot(sol_prog_8);
plot(sol_prog_9);
plot(sol_prog_10);
plot(sol_prog_11);
legend('Crossover = 0.6, Mutation = 0.25',...
    'Crossover = 0.3, Mutation = 0.125',...
    'Crossover = 0.8, Mutation = 0.125',...
    'Crossover = 0.3, Mutation = 0.75',...
    'Crossover = 0.8, Mutation = 0.75');
hold off;