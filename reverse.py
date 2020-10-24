import pylp
import numpy as np
import copy

from game_of_life import step, init_random, get_neighborhood

def set_backend():
    try:
        backend = pylp.create_linear_solver(pylp.Preference.Gurobi) 
    except:
        # Fallback no gurobi
        print("Gurobi not available, use Scip...")
        backend = pylp.create_linear_solver(pylp.Preference.Scip) 
    
    return backend

def reverse(target_state):
    """
    Reverse one step of the game of life
    given a target state.

    target_state: 2D array of bools

    returns: prior state such that one step
    of the game of life evolution leads to
    the target state.
    """

    state_shape = np.shape(target_state)
    assert(len(state_shape) == 2)
    n_variables = state_shape[0] * state_shape[1] # One binary var for each pixel

    backend = set_backend()
    backend.initialize(2*n_variables, pylp.VariableType.Binary)
    objective = pylp.LinearObjective(2*n_variables) 
    constraints = pylp.LinearConstraints()
    variable_map = {}
    variable_map_inverse = {}

    # Mapping from variables to pixels
    k = 0
    for i in range(state_shape[0]):
        for j in range(state_shape[1]):
            variable_map[k] = (i,j)
            variable_map_inverse[(i,j)] = k
            k += 1

    for i in range(state_shape[0]):
        for j in range(state_shape[1]):
            center_var = variable_map_inverse[(i,j)]
            delta = center_var + n_variables
            # Set placeholder objective maximizing alive cells:
            objective.set_coefficient(center_var, -1)

            nbs = get_neighborhood(i,j, state_shape[0], state_shape[1])
            nbs_vars = [variable_map_inverse[v] for v in nbs]
    
            if target_state[i,j]:
                constraint = pylp.LinearConstraint()
                for var in nbs_vars:
                    constraint.set_coefficient(var, 1)
                constraint.set_relation(pylp.Relation.LessEqual)
                constraint.set_value(3)
                constraints.add(constraint)

                constraint = pylp.LinearConstraint()
                for var in nbs_vars:
                    constraint.set_coefficient(var, 1)
                constraint.set_coefficient(center_var, -2)
                constraint.set_relation(pylp.Relation.GreaterEqual)
                constraint.set_value(0)
                constraints.add(constraint)
            
                constraint = pylp.LinearConstraint()
                for var in nbs_vars:
                    constraint.set_coefficient(var, 1)
                constraint.set_coefficient(center_var, 3)
                constraint.set_relation(pylp.Relation.GreaterEqual)
                constraint.set_value(3)
                constraints.add(constraint)

            if not target_state[i,j]:
                constraint = pylp.LinearConstraint()
                for var in nbs_vars:
                    constraint.set_coefficient(var, 1)
                constraint.set_coefficient(center_var, 1)
                constraint.set_coefficient(delta, -8)
                constraint.set_relation(pylp.Relation.LessEqual)
                constraint.set_value(2)
                constraints.add(constraint)

                constraint = pylp.LinearConstraint()
                for var in nbs_vars:
                    constraint.set_coefficient(var, 1)
                constraint.set_coefficient(delta, -4)
                constraint.set_relation(pylp.Relation.GreaterEqual)
                constraint.set_value(0)
                constraints.add(constraint)

    backend.set_constraints(constraints)
    solution, msg = backend.solve()
    print("SOLVED with status: " + msg)

    prior_state = np.zeros(state_shape, dtype=bool)
    for var in range(n_variables):
        i,j = variable_map[var]
        if solution[var] > 0.5:
            prior_state[i,j] = True

    return prior_state

def init_state():
    simple_state = np.zeros((10,10), dtype=bool)
    simple_state[3,3] = 1
    return simple_state
          
if __name__ == "__main__":
    #simple_state = init_state()
    random_state = init_random(5,5)
    one_step = step(random_state)
    two_step = step(one_step)

    two_step_copy = copy.deepcopy(two_step)
    prior_state = reverse(two_step_copy)
    prior_state_copy = copy.deepcopy(prior_state)
    two_step_2 = step(prior_state_copy)

    print("reversed", prior_state.astype(int))
    print("step 1", one_step.astype(int))
    print("reversed_step", two_step_2.astype(int))
    print("step 2", two_step.astype(int))
    print("Diff rev - step 2")
    print(two_step.astype(int) - two_step_2.astype(int))
