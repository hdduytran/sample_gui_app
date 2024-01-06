import concurrent.futures
import os
from functools import wraps

def make_parallel(func):
    """
        Decorator used to decorate any function which needs to be parallized.
        After the input of the function should be a list in which each element is a instance of input fot the normal function.
        You can also pass in keyword arguements seperatley.
        :param func: function
            The instance of the function that needs to be parallelized.
        :return: function

        Example usage:
        @make_parallel
        def func(i: int):
            print(i)
        func([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    """

    @wraps(func)
    def wrapper(lst, *args, **kwargs):
        """
        :param lst:
            The inputs of the function in a list.
        :return:
        """
        # number_of_workers = int(os.cpu_count() * 2)
        number_of_workers = 4
        # if len(lst) < number_of_workers:
        #     number_of_workers = len(lst)

        result = []
        if number_of_workers:
            if number_of_workers == 1:
                result = [func(lst[0], *args, **kwargs)]
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:
                    bag = {executer.submit(
                        func,  i, *args, **kwargs): i for i in lst}
                    for future in bag:
                        result.append(future.result())

        # remove None value
        result = [i for i in result if i]
        return result
    return wrapper
