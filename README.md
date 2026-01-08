# Overview

Benchmarking various implementations of readers-writer locks, `std::sync::RwLock`, `parking_lot::RwLock`, `tokio::sync::RwLock`. We compare several different Rust implementations of readers-writer locks.

 - [pflock](https://crates.io/crates/pflock), based on "Reader-writer synchronization for shared-memory multiprocessor real-time systems"
 - [pairlock](https://crates.io/crates/pairlock)
 - [tokio](https://tokio.rs/)
 - [sharedmutex](https://crates.io/crates/shared-mutex)
 - [widerwlock](https://crates.io/crates/widerwlock)
 - [spin](https://crates.io/crates/spin)
 - [std::sync::RwLock](https://doc.rust-lang.org/std/sync/struct.RwLock.html)
 - [crossbeam::ShardedLock](https://docs.rs/crate/crossbeam/)

## Running Benchmarks

The benchmarks are implemented in [Rust](https://www.rust-lang.org/) using the [Criterion](https://crates.io/crates/criterion) benchmarking library. They can be ran using the `run.py` script:

```bash
    python run.py results/
```

From these results the table can be generated as follows:

```bash
    python generate_table.py results/benchmarks.json
```