from __future__ import annotations

import uvicorn


def main():
    uvicorn.run(
        'rea_beta_backend_toolsets.app.main:app',
        host='127.0.0.1', port=8000, reload=True,
    )


if __name__ == '__main__':
    main()
