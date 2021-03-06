# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher


@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    def __init__(self):
        self.descr = 'STREAM Benchmark'
        self.exclusive_access = True
        self.valid_systems = ['kebnekaise:%s' % x for x in ['bdw', 'sky', 'knl', 'lm']]
        self.valid_prog_environs = ['foss', 'intel']

        #self.use_multithreading = False

        self.prgenv_flags = {
            'foss': ['-fopenmp', '-O3', '-march=native', '-static'],
            'intel': ['-qopenmp', '-O3', '-xHost', '-ip', '-ansi-alias', '-fno-alias', '-static', '-qopt-prefetch-distance=64,8', '-qopt-streaming-cache-evict=0', '-qopt-streaming-stores always'],
        }

        self.build_locally = False
        self.sourcepath = 'stream.c'
        self.build_system = 'SingleSource'
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.stream_cpus_per_task = {
            'kebnekaise:bdw': 28,
            'kebnekaise:sky': 28,
            'kebnekaise:gpu': 28,
            'kebnekaise:knl': 68,
            'kebnekaise:lm': 72,
        }
        # Size of array in Mi-elements (*1024^2), total memory usage is size * 1024^2 * 8 * 3
        self.stream_array = {
            'kebnekaise:bdw': 4500,
            'kebnekaise:sky': 4500,
            'kebnekaise:gpu': 4500,
            'kebnekaise:knl': 6800,
            'kebnekaise:lm': 24000, # 121000, for using the whole memory, but that takes forever.
        }
        self.variables = {
            'OMP_PLACES': 'threads',
            'OMP_PROC_BIND': 'spread'
        }
        self.sanity_patterns = sn.assert_found(
            r'Solution Validates: avg error less than', self.stdout)
        self.perf_patterns = {
            'copy': sn.extractsingle(r'^Copy:\s+(?P<copy>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'copy', float),
            'scale': sn.extractsingle(r'^Scale:\s+(?P<scale>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'scale', float),
            'add': sn.extractsingle(r'^Add:\s+(?P<add>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'add', float),
            'triad': sn.extractsingle(r'^Triad:\s+(?P<triad>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'triad', float),
        }
        self.stream_bw_reference = {
            'foss': {
                'kebnekaise:bdw': {
                    'copy':  (74000, -0.05, 0.05, 'MB/s'),
                    'scale': (74000, -0.05, 0.05, 'MB/s'),
                    'add':   (84500, -0.05, 0.05, 'MB/s'),
                    'triad': (84500, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:sky': {
                    'copy':  (103900, -0.05, 0.05, 'MB/s'),
                    'scale': (103900, -0.05, 0.05, 'MB/s'),
                    'add':   (116700, -0.05, 0.05, 'MB/s'),
                    'triad': (116700, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:knl': {
                    'copy':  (57000, -0.05, 0.05, 'MB/s'),
                    'scale': (56000, -0.05, 0.05, 'MB/s'),
                    'add':   (63000, -0.05, 0.05, 'MB/s'),
                    'triad': (63000, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:lm': {
                    'copy':  (191500, -0.05, 0.05, 'MB/s'),
                    'scale': (191500, -0.05, 0.05, 'MB/s'),
                    'add':   (198000, -0.05, 0.05, 'MB/s'),
                    'triad': (198000, -0.05, 0.05, 'MB/s'),
                },
            },
            'intel': {
                'kebnekaise:bdw': {
                    'copy':  (120500, -0.05, 0.05, 'MB/s'),
                    'scale': (120500, -0.05, 0.05, 'MB/s'),
                    'add':   (108000, -0.05, 0.05, 'MB/s'),
                    'triad': (108000, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:sky': {
                    'copy':  (155000, -0.05, 0.05, 'MB/s'),
                    'scale': (155000, -0.05, 0.05, 'MB/s'),
                    'add':   (113000, -0.05, 0.05, 'MB/s'),
                    'triad': (115000, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:knl': {
                    'copy':  (57000, -0.05, 0.05, 'MB/s'),
                    'scale': (57000, -0.05, 0.05, 'MB/s'),
                    'add':   (57900, -0.05, 0.05, 'MB/s'),
                    'triad': (57900, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:lm': {
                    'copy':  (233000, -0.05, 0.05, 'MB/s'),
                    'scale': (228000, -0.05, 0.05, 'MB/s'),
                    'add':   (225000, -0.05, 0.05, 'MB/s'),
                    'triad': (230000, -0.05, 0.05, 'MB/s'),
                },
            },
        }
        self.tags = {'production'}
        self.maintainers = ['??S']

    @run_after('setup')
    def prepare_test(self):
        self.num_cpus_per_task = self.stream_cpus_per_task.get(
            self.current_partition.fullname, 1)
        self.extra_resources = {
            'threads': {'threads': 4},
        }

        omp_threads = self.num_cpus_per_task
        if self.current_partition.fullname == 'kebnekaise:knl':
            omp_threads *= 4
        
        self.variables['OMP_NUM_THREADS'] = str(omp_threads)
        envname = self.current_environ.name

        self.build_system.cflags = self.prgenv_flags.get(envname, ['-O3'])

        try:
            self.reference = self.stream_bw_reference[envname]
        except KeyError:
            self.reference = self.stream_bw_reference['foss']

    # Stream is serial or OpenMP and should not be started by srun.
    # Especially on the KNLs where that may cause bad thread placement.
    @run_after('setup')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    @run_before('run')
    def set_array_size(self):
        mem_sz = self.stream_array.get(self.current_partition.fullname, 2500)*1024*1024
        self.executable_opts = ["-s", "%s" % mem_sz]

    @run_after('run')
    def set_nodelist(self):
        self.mynodelist = self.job.nodelist
