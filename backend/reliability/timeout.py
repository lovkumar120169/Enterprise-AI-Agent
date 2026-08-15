from concurrent.futures import ThreadPoolExecutor, TimeoutError


def run_with_timeout(
    func,
    timeout_seconds: float,
    *args,
    **kwargs
):

    with ThreadPoolExecutor(
        max_workers=1
    ) as executor:

        future = executor.submit(
            func,
            *args,
            **kwargs
        )

        try:

            return future.result(
                timeout=timeout_seconds
            )

        except TimeoutError:

            future.cancel()

            raise TimeoutError(
                f"{func.__name__} timed out after "
                f"{timeout_seconds} seconds"
            )