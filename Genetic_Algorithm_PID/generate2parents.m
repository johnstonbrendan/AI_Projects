function [parent1,parent2,fitness_nums] = generate2parents(chromozones)
%GENERATE2PARENTS Generates 2 parents from current chromozones
%   Generates parents based off FPS

% Calculate total fitness
total_fitness = 0;
fitness_nums = double(chromozones(:,2));
max_fitness = max(fitness_nums) + 1;

for i = 1:length(fitness_nums)
    fitness_nums(i) = max_fitness - fitness_nums(i);
    total_fitness = total_fitness + fitness_nums(i);
end

p1_index = 1; % This is the selected index
p2_index = 1;
rand_val = rand();
cum_prob = 0;
max_fitness = max_fitness + 1;

% Calculate
for i = 1:length(fitness_nums)
    if rand_val < cum_prob
        p1_index = i;
        fitness_nums(i) = 0;
        break
    else
        cum_prob = cum_prob + fitness_nums(i)/total_fitness;
    end
end

cum_prob = 0;
rand_val = rand();
for i = 1:length(fitness_nums)
    if rand_val < cum_prob % make the first cum_prob rand_val
        p2_index = i;
        break
    else
        cum_prob = cum_prob + fitness_nums(i)/total_fitness;
    end
end

parent1 = chromozones(p1_index,1);
parent2 = chromozones(p2_index,1);



    

