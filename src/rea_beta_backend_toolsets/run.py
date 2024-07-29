from __future__ import annotations

import logging.config
import logging.handlers

from rea_beta_backend_toolsets.services.logging.logger import setup_logging
# import uvicorn

logger = logging.getLogger('rea_proxy')


def main():
    setup_logging()
    logging.basicConfig(level='INFO')
    logging.info('hello world')
    # uvicorn.run(
    #     'rea_beta_backend_toolsets.app.main:app',
    #     host='127.0.0.1', port=8000, reload=True,
    # )


if __name__ == '__main__':
    main()
