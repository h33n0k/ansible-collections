# 🌐 NTP Protocols Overview

This document provides a concise explanation of the **Network Time Protocol (NTP)** and related protocols used for synchronizing system clocks across networked machines.

Accurate time synchronization is essential for logging, scheduling, authentication, and maintaining consistency across distributed systems. NTP is the standard protocol used to achieve this.

---

## Table of Contents
- [🧭 What is NTP?](#-what-is-ntp)
- [🧱 NTP Stratum Levels](#-ntp-stratum-levels)
- [🔎 Simplified NTP Variants](#-simplified-ntp-variants)
- [📦 NTP in Practice (Debian)](#-ntp-in-practice-debian)
- [🛠️ Common Time Synchronization Tools on Debian](#-common-time-synchronization-tools-on-debian)
- [📡 Recommended Public NTP Pools](#-recommended-public-ntp-pools)
- [✅ Best Practices](#-best-practices)

---

## 🧭 What is NTP?

**Network Time Protocol (NTP)** is a networking protocol designed to synchronize the clocks of computers over packet-switched, variable-latency data networks.

- **Defined by**: [RFC 5905](https://datatracker.ietf.org/doc/html/rfc5905)
- **Operates over**: UDP port 123
- **Accuracy**: Millisecond to sub-millisecond precision on LANs; typically a few milliseconds over the public Internet.

---

## 🧱 NTP Stratum Levels

NTP servers and clients form a layered hierarchy:

<details>
NTP is a time protocol for network equipment which has a tree-like architecture. Each level of the hierarchy is called a stratum. The standard has a limit of 16 stratums. Servers from the same stratum share a common time reference that they send to the following stratrum.  

Stratum 0 is made up of reference clocks which can be atomic clocks, GPS clocks, and so on. These are the root machines of the protocol, responsible for providing the exact time. They will maintain what is known as UTC time.  

Stratum 0 is connected to stratum 1 via serial ports. Stratum 1 is made up of primary NTP servers. These will broadcast the synchronization timestamps to the rest of the network. There are several stratum 1 servers available publicly both in France and internationally. However, it is not recommended to connect to them, and here’s why: Servers in stratum 2 to stratum 15 synchronize with higher-stratum servers. These may also peer with other servers at the same stratum for redundancy.
</details>

| Stratum | Description                             |
|---------|-----------------------------------------|
| 0       | High-precision time source (e.g. GPS, atomic clock) — not network-connected |
| 1       | Directly connected to a Stratum 0 source |
| 2       | Synchronizes with Stratum 1 server       |
| 3+      | Synchronizes with higher stratum levels  |

![bodet-time.com](https://static.bodet-time.com/images/stories/blog/fonctionnement-strates-ntp.jpg)

source: [STRATUMS IN THE NTP PROTOCOL: Understanding the hierarchy of servers](https://www.bodet-time.com/resources/blog/1882-stratums-in-the-ntp-protocol-understanding-the-hierarchy-of-servers.html)

Clients should use **multiple servers** at different strata to avoid single points of failure and improve accuracy.

---

## 🔎 Simplified NTP Variants

### SNTP (Simple NTP)
- Follows the basic structure of NTP, but with fewer features and less accuracy.
- Common in embedded systems or environments with minimal sync requirements.
- Used by `systemd-timesyncd`.

### Precision Time Protocol (PTP)
- Defined in [IEEE 1588](https://ieeexplore.ieee.org/document/9120376).
- Offers **sub-microsecond accuracy** over local area networks.
- Used in **real-time** or **high-frequency** environments (e.g., telecom, trading systems).
- Not supported by typical NTP daemons like `ntpd` or `timesyncd`.

| Feature | NTP | SNTP | PTP |
|--------|-----|------|----|
| **Accuracy** | ms | ~ms | µs |
| **Protocol** | `RFC 5905` | `RFC 4330` | `IEEE 1588` |
| **Use Case** | General | Embedded, lightweight | Real-time systems |
| **Transport** | UDP:123 | UDP:123 | Ethernet/UDP |

---

## 📦 NTP in Practice (Debian)

- Debian ships with `systemd-timesyncd` by default.
- It uses SNTP to periodically query configured NTP servers.
- For general-purpose workloads, SNTP via `systemd-timesyncd` is **sufficient and preferred**.
- For environments with strict accuracy or compliance needs, full NTP or PTP daemons may be required.

### `timesyncd` example config snippet:
```ini
[Time]
NTP=0.arch.pool.ntp.org 1.arch.pool.ntp.org 2.arch.pool.ntp.org 3.arch.pool.ntp.org
FallbackNTP=0.pool.ntp.org 1.pool.ntp.org

RootDistanceMaxSec=5
PollIntervalMinSec=32
PollIntervalMaxSec=2048
ConnectionRetrySec=30
SaveIntervalSec=60
```

### `timdatectl status` example output:
```
               Local time: Sun 2025-04-20 18:00:08 CEST
           Universal time: Sun 2025-04-20 16:00:08 UTC
                 RTC time: Sun 2025-04-20 16:00:08
                Time zone: Europe/Paris (CEST, +0200)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

While `systemd-timesyncd` is the default NTP client on most Debian systems, several other tools exist—each with their own strengths, trade-offs, and ideal use cases. Understanding these tools is key to selecting the right one for your system’s accuracy, reliability, and performance needs.

## 🛠️ Common Time Synchronization Tools on Debian

Debian systems support multiple time synchronization tools, each suited for different use cases and accuracy requirements. Here are the most commonly used ones:

### `systemd-timesyncd`
A lightweight SNTP client bundled with `systemd`. It is the default on most modern Debian systems. It provides basic time synchronization suitable for general-purpose workloads and does not require separate installation.

- ✅ Integrated with `systemd`
- ✅ Simple to configure
- ❌ No support for NTP authentication or advanced algorithms

### `ntpd`
The reference implementation of the full **NTPv4** protocol. It provides accurate time synchronization, support for complex configurations, and features like clock discipline and authentication. However, it is considered more heavyweight and is gradually being replaced by alternatives in some environments.

- ✅ Long-time standard, robust
- ✅ Supports complex setups, GPS, serial reference clocks
- ❌ Slower to converge, higher resource usage

### `chronyd`
An advanced and efficient NTP daemon, often used in cloud or virtualized environments. It is designed to handle unstable networks and quick system clock adjustments (even when offline). It supports **NTS** (NTP over TLS) and performs well in constrained or mobile environments.

- ✅ High precision and fast convergence
- ✅ Handles sleep/wake and VM migration well
- ✅ Supports NTS (secure time sync)
- ❌ Slightly more complex configuration than `timesyncd`

---

The table below summarizes the key differences between these tools:

| Feature / Client | `systemd-timesyncd` | `ntpd` | `chronyd` |
|------------------|---------------------|--------|-----------|
| **Accuracy** | ~100 ms | ~10 ms | <1 ms (LAN), ~10 ms (WAN) |
| **Protocol Support** | SNTP | Full NTPv4 | Full NTPv4 |
| **Startup Time** | Fast | Moderate | Fast |
| **Resource Usage** | Very low | Moderate | Low |
| **Network Jitter Handling** | Basic | Good | Excellent |
| **Time Slewing** | Basic | Yes | Adaptive & precise |
| **Authentication Support** | No | Yes (symmetric keys, autokey) | Yes (symmetric, NTS optional) |
| **TLS Support** | No | With wrapper (e.g. NTS patch) | Yes (via NTS, Chrony ≥4.0) |
| **Monitoring Tools** | `timedatectl` | `ntpq`, `ntpstat` | `chronyc`, `chrony sources` |
| **Default on Debian** | ✅ Yes (minimal systems) | ❌ Optional | ❌ Optional |
| **Ideal Use Case** | Lightweight, general systems  | Traditional setups, RFC compliance | Precise timekeeping, mobile devices, VMs |

**Recommendation**:
- For **most users**, `systemd-timesyncd` is sufficient and simple.
- Use `chronyd` in **virtualized**, **battery-powered**, or **low-jitter environments**.
- Use `ntpd` if you need **strict RFC 5905 compliance** or legacy compatibility.

---

## 📡 Recommended Public NTP Pools

When not using internal time sources, trusted public pools include:

- `0.debian.pool.ntp.org`
- `1.debian.pool.ntp.org`
- `time.cloudflare.com`
- `pool.ntp.org`

Always use at least **3–4 servers** to ensure accuracy and fault tolerance.

---

## ✅ Best Practices

- Avoid using only one NTP server—redundancy improves accuracy and reliability.
- Use local/internal NTP servers for faster convergence in private infrastructure.
- Reduce the number of internal stratums in private infrastructure
- Place machines with an identical role in the same stratum
- Monitor time sync status with `timedatectl` or `ntpq -p` (when using a full NTP daemon).
- Gradual adjustments are safer than stepping the clock, especially for running applications.

Organise your network structure correctly and choose the right equipment so that critical applications can rely on efficient time synchronization.

---

📘 *See also*: [RFC 5905 - NTPv4](https://datatracker.ietf.org/doc/html/rfc5905), [1588-2019 - IEEE](https://ieeexplore.ieee.org/document/9120376), [systemd-timesyncd man page](https://www.freedesktop.org/software/systemd/man/systemd-timesyncd.service.html)
