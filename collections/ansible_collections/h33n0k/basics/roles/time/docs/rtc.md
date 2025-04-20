# Real-Time Clock (RTC) on Debian

This document provides an overview of the **Real-Time Clock (RTC)** on Debian systems, including its purpose, how it interacts with the system clock, and how to configure and verify its behavior.

## Table of Contents
- [🧠 What is the RTC?](#-what-is-the-rtc)
- [🔄 RTC vs System Clock](#-rtc-vs-system-clock)
- [🔍 Inspecting RTC Settings](#-inspecting-rtc-settings)
- [⚙️ Configuring RTC](#-configuring-rtc)
- [📦 How Debian Uses the RTC](#-how-debian-uses-the-rtc)
- [✅ Best Practices](#-best-practices)

---

## 🧠 What is the RTC?

The **Real-Time Clock (RTC)** is a small, battery-backed hardware clock embedded on your motherboard.

- Keeps track of time while the system is powered off.
- Often implemented as `/dev/rtc0` or `/dev/rtc`.

It maintains basic calendar time (year, month, day, hour, minute, second), but usually **not time zones** or **NTP sync**.

---

## 🔄 RTC vs System Clock

Debian maintains two clocks:

| Clock Type | Maintains Time While Off | Affected by Timezone | Synchronized with NTP |
|------------|--------------------------|----------------------|-----------------------|
| **RTC** | ✅ Yes | ❌ No | 🚫 Not directly |
| **System Clock** | ❌ No | ✅ Yes | ✅ Yes|

At boot:
- The kernel **reads the RTC** and initializes the system clock.
- Once up, **NTP or timesyncd** keeps the system clock accurate.
- RTC can be updated periodically from system time (e.g., via `hwclock --systohc`).

---

## 🔍 Inspecting RTC Settings

Use `timedatectl` to view RTC status:
```bash
timedatectl
```

Example:
```
               Local time: Sun 2025-04-20 18:00:08 CEST
           Universal time: Sun 2025-04-20 16:00:08 UTC
                 RTC time: Sun 2025-04-20 16:00:08
                Time zone: Europe/Paris (CEST, +0200)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

### 🔧 Check raw RTC time:
```bash
sudo hwclock --show
```

---

## ⚙️ Configuring RTC

### ⏱️ Sync system clock to RTC:
```bash
sudo hwclock --systohc
```

### 🔄 Sync RTC to system clock (e.g. after NTP sync):
```bash
sudo hwclock --hctosys
```

### 🌐 Set RTC to UTC (recommended for Linux servers):
```bash
sudo timedatectl set-local-rtc 0 --adjust-system-clock
```

This ensures RTC is in UTC and system handles timezone separately.

### 🏠 Set RTC to local time (for dual-boot with Windows):
```bash
sudo timedatectl set-local-rtc 1 --adjust-system-clock
```

Windows expects RTC in local time; this is a workaround but not ideal.

---

## 📦 How Debian Uses the RTC

- Debian automatically reads RTC at boot to initialize the system clock.
- `systemd-timesyncd` (or another NTP daemon) syncs system clock later.
- RTC updates are typically **not automatic**, unless configured by `hwclock` or `systemd`.

Relevant systemd service:
```bash
systemctl status hwclock.service
```

---

## ✅ Best Practices

- ⏰ **Set RTC to UTC** unless dual-booting with Windows.
- 🧽 Periodically **sync RTC from system time** if NTP is active.
- 🧪 Always verify RTC status after making changes.
- 🔒 Ensure `/etc/adjtime` is consistent with your UTC/local policy:
  - Contents:
    ```ini
    0.0 0 0
    0
    UTC
    ```

---

📘 *See also*:
- [`timedatectl` man page](https://www.freedesktop.org/software/systemd/man/timedatectl.html)
- [`hwclock` man page](https://man7.org/linux/man-pages/man8/hwclock.8.html)
- [Debian Wiki: Time](https://wiki.debian.org/Time)
