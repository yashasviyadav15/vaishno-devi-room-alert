# Vaishno Devi Room Availability Alert

Checks the Vaishno Devi accommodation availability endpoint and emails an alert when rooms are available.

## API request

The script currently checks:

- Date: 2026-11-09
- Location ID: 3
- Accommodation type ID: 1
- Stay: 1 day

## Run locally

Install Python 3.10+ and run:

```bash
pip install -r requirements.txt
```

Set these environment variables:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=your@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_TO=destination@example.com
```

Then:

```bash
python check_rooms.py
```

## GitHub Actions

1. Create a GitHub repository.
2. Upload this repository's files.
3. Go to **Settings → Secrets and variables → Actions**.
4. Add:
   - `EMAIL_FROM`
   - `EMAIL_PASSWORD`
   - `EMAIL_TO`
5. Go to **Actions → Check Vaishno Devi Rooms → Run workflow** to test immediately.

The workflow is scheduled for approximately every 10 minutes.

## Availability logic

A room is considered available when:

- `flag` is `"N"`
- `accomAvailOp` is not null
- `noOfAvailable` is greater than 0

No email is sent when no qualifying room is returned.

## Security

Never commit your Gmail App Password or other credentials to the repository. Use GitHub Actions Secrets.
