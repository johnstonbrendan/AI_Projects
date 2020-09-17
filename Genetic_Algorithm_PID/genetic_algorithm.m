function [best_fit_per_gen,best_PID] = genetic_algorithm(generations,...
                    population,crossover_probability,mutation_probability)

% Steps
% Start by generating 50 random chromozones

tot_gens = generations;
pop = population;
crs_prob = crossover_probability;
mut_prob = mutation_probability;


chromos = strings(pop,1);
for i = 1:pop
    val = dec2bin(randi(536870911),29);
    chromos(i,1) = val;
    % Evaluate their fitness
    chromos(i,2) = fitness(chrom2param(val));
    % 536870911 = 2^29 - 1 the max chomrozone val
end


% Find the best 2, store them somewherer
chromos = sortrows(chromos,2);
elite_chromos = chromos(1:2,:);
best_chrom_per_gen = strings(tot_gens,2);

for gen = 1:tot_gens
    cur_gen = gen
    % Shuffle 50 chromozones
    child_chromos = strings(pop,1);
    chromos = chromos(randperm(length(chromos)),:); 
    % You can change the 1 in the line above to : if you want to keep
    % fitness scores, but you don't need them after shuffling (or vicevers)
    
    % apply cross over and mutation to all with the probabilities
    chromos_len = length(chromos);
    for i = 1:chromos_len
        [parent1,parent2] = generate2parents(chromos);
        if rand() < crs_prob
            child_chromos(i,1) = ...
                       crossover(parent1,parent2);
        else
            child_chromos(i,1) = parent1;
        end
        if rand() < mut_prob
            child_chromos(i,1) = mutate(child_chromos(i,1));
        end
        % evaluate all the fitness
        child_fit = fitness(chrom2param(child_chromos(i,1)));
        child_chromos(i,2) = child_fit;
    end
    child_chromos = [child_chromos;elite_chromos];
    child_chromos = sortrows(child_chromos,2);
    chromos = child_chromos(1:end-2,:);
    elite_chromos = chromos(1:2,:);
    best_chrom_per_gen(gen,:) = chromos(1,:);
end

best_PID = chrom2param(chromos(1,:));
best_fit_per_gen = double(best_chrom_per_gen(:,2));

end

% loop
% shuffle the 50 chromozones
% use russian roulette to remove 2 of the chromozones, you want to remove
% the weakest ones, so set the probability to be 1 - fitness/total_fitness
% and select ones to remvoe based off this.
% add the two best from before to now make the population back to 50
% find the two best, store them

% Need to do a float 2 binary and as well as a K_p T_... to chrom