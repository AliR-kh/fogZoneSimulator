import random
import datetime as dt
from utilize.Execution.execut import Execut as EX

class MS_PSO:
    def __init__(
        self,
        particle_count=20,
        iterations=10,
        c1=2.0,
        c2=2.0,
        num_swarms=3,
        migration_interval=5,     # هر چند iteration یک بار مهاجرت
        elite_fraction=0.2,       # درصد ذرات نخبه برای مهاجرت
        share_global_every=3      # هر چند iteration یک بار gbest سراسری را تزریق می‌کنیم
    ):
        # پارامترهای پایه PSO
        self.particle_count = particle_count
        self.iterations = iterations
        self.c1 = c1
        self.c2 = c2
        self.W = 1

        # نرمال‌سازی/رِنج‌ها (هم‌نام با کلاس شما برای سازگاری)
        self.MSmax = 1
        self.MSmin = 0
        self.TCmax = 0
        self.TCmin = 0
        self.TEmax = 0
        self.TEmin = 0
        self.LBCmax = 0
        self.LBCmin = 0
        self.LBFmax = 0
        self.LBFmin = 0

        # پارامترهای چند-سوارمی
        self.num_swarms = max(1, int(num_swarms))
        self.migration_interval = max(1, int(migration_interval))
        self.elite_fraction = max(0.0, min(0.5, float(elite_fraction)))
        self.share_global_every = max(1, int(share_global_every))

    # --------- ابزار داخلی ---------
    def _init_particle(self, jobs, resources, edges):
        position = [random.randint(0, len(resources) - 1) for _ in range(len(jobs))]
        velocity = [random.uniform(0.0, 1.0) for _ in range(len(jobs))]
        pbest = position.copy()
        pbest_fitness = self.fitness(position, jobs, edges, resources)
        return (position, velocity, pbest, pbest_fitness)

    def _split_into_swarms(self, particles):
        # توزیع ذرات به چند سوارم با حداقل اختلاف
        swarms = [[] for _ in range(self.num_swarms)]
        for i, p in enumerate(particles):
            swarms[i % self.num_swarms].append(p)
        return swarms

    def _best_of_swarm(self, swarm):
        # پیدا کردن gbest سوارم
        gbest = None
        gbest_fit = float('-inf')
        for (pos, vel, pbest, pbest_fit) in swarm:
            if pbest_fit > gbest_fit:
                gbest_fit = pbest_fit
                gbest = pbest.copy()
        return gbest, gbest_fit

    def _best_overall(self, swarms):
        # gbest سراسری از بین همه سوارم‌ها
        gbest = None
        gbest_fit = float('-inf')
        for swarm in swarms:
            sbest, sbest_fit = self._best_of_swarm(swarm)
            if sbest_fit > gbest_fit:
                gbest_fit = sbest_fit
                gbest = sbest.copy()
        return gbest, gbest_fit

    # --------- رابط مشابه PSO شما ---------
    def initialize_swarm(self, resources, jobs, edges):
        # تولید همه ذرات و سپس تقسیم به سوارم‌ها
        particles = [self._init_particle(jobs, resources, edges) for _ in range(self.particle_count)]
        swarms = self._split_into_swarms(particles)

        # gbest سراسری
        gbest, gbest_fitness = self._best_overall(swarms)
        return gbest, swarms

    def update_swarm(self, swarm, gbest_swarm, resources, jobs, edges):
        # به‌روزرسانی یک سوارم با استفاده از gbest خودش
        for i in range(len(swarm)):
            position, velocity, pbest, pbest_fitness = swarm[i]

            new_velocity = [
                self.calculate_new_velocity(velocity[d], pbest[d], position[d], gbest_swarm[d])
                for d in range(len(position))
            ]
            # موقعیت عدد صحیح و داخل محدوده‌ی منابع
            new_position = [
                max(0, min(int(position[d] + new_velocity[d]), len(resources) - 1))
                for d in range(len(position))
            ]

            new_fitness = self.fitness(new_position, jobs, edges, resources)

            # به‌روزرسانی pbest
            if new_fitness > pbest_fitness:
                pbest = new_position.copy()
                pbest_fitness = new_fitness

            swarm[i] = (new_position, new_velocity, pbest, pbest_fitness)

        # gbest این سوارم
        gbest_swarm, gbest_fitness = self._best_of_swarm(swarm)
        return gbest_swarm, gbest_fitness

    def _migrate_between_swarms(self, swarms):
        # مهاجرت ذرات نخبه بین سوارم‌ها به‌صورت حلقه‌ای
        if self.elite_fraction <= 0:
            return

        k_list = [max(1, int(len(s)*self.elite_fraction)) for s in swarms]
        # برای هر سوارم: نخبه‌ها را به سوارم بعدی بده، بدترین‌ها را جایگزین کن
        for idx, swarm in enumerate(swarms):
            if len(swarm) == 0:
                continue
            k = k_list[idx]

            # مرتب‌سازی بر حسب pbest_fitness
            sorted_swarm = sorted(swarm, key=lambda t: t[3], reverse=True)
            elites = sorted_swarm[:k]
            # مقصد حلقه‌ای
            dst_idx = (idx + 1) % len(swarms)
            dst_swarm = swarms[dst_idx]

            if len(dst_swarm) == 0:
                continue

            # بدترین‌ها در مقصد
            dst_sorted = sorted(dst_swarm, key=lambda t: t[3])
            replace_count = min(k, len(dst_swarm))

            # جایگزینی
            for r in range(replace_count):
                dst_swarm[dst_swarm.index(dst_sorted[r])] = elites[r]

            swarms[idx] = sorted_swarm  # نگه داشتن ترتیب به‌روز شده (اختیاری)

    def run(self, resources, jobs, edges):
        gbest_global, swarms = self.initialize_swarm(resources, jobs, edges)

        for it in range(self.iterations):
            # هر سوارم با gbest خودش آپدیت می‌شود
            for s_idx in range(len(swarms)):
                gbest_swarm, _ = self._best_of_swarm(swarms[s_idx])
                gbest_swarm, _ = self.update_swarm(
                    swarms[s_idx],
                    gbest_swarm,
                    resources,
                    jobs,
                    edges
                )

            # gbest سراسری را محاسبه و گاهی به همه تزریق می‌کنیم
            gbest_global, _ = self._best_overall(swarms)
            if (it + 1) % self.share_global_every == 0:
                # تزریق: نصف ذرات بدترین هر سوارم gbest سراسری را به عنوان pbest می‌گیرند
                for s in swarms:
                    if not s:
                        continue
                    half = max(1, len(s)//2)
                    s_sorted = sorted(s, key=lambda t: t[3])  # بدترین‌ها اول
                    for i in range(half):
                        pos, vel, pbest, pbest_fit = s_sorted[i]
                        # تزریق دانشِ جمعی
                        pbest = gbest_global.copy()
                        pbest_fit = self.fitness(pbest, jobs, edges, resources)
                        s[s.index(s_sorted[i])] = (pos, vel, pbest, pbest_fit)

            # مهاجرت نخبه‌ها بین سوارم‌ها
            if (it + 1) % self.migration_interval == 0:
                self._migrate_between_swarms(swarms)

        # گلوبال بهترین در پایان
        gbest_global, _ = self._best_overall(swarms)
        return self.prepare_result(gbest_global, resources, jobs)

    def prepare_result(self, gbest, resources, jobs):
        # همان فرمت خروجی شما
        finall_result = []
        vmnumb = len(resources) - 1
        for i in range(len(jobs)):
            if gbest[i] == vmnumb:
                finall_result.append({"type": "Edge", "id": jobs[i][0]})
            else:
                finall_result.append({
                    "type": resources[gbest[i]]["type"],
                    "id": resources[gbest[i]]["id"]
                })
        return finall_result

    # --- همان امضا و منطق، ولی return اشتباهی داخل حلقه حذف شده تا جمع درست محاسبه شود ---
    def fitness(self, position, job, edge, resources):
        total_result = 0.0
        vmnumb = len(resources) - 1

        for jobnumb in range(len(job)):
            device_id = job[jobnumb][0]
            task_id = job[jobnumb][1]

            # تعیین VM انتخابی برای این تسک
            selected_vm = None
            mips = None

            # پیدا کردن edge مربوط به device
            for devnumb in range(1, len(edge)):
                if device_id == edge[devnumb]["id"]:
                    if position[jobnumb] == vmnumb:
                        vm = edge[devnumb]["specif"]
                        mips = float(vm["mips"])
                    else:
                        vm = resources[position[jobnumb]]
                        mips = float(vm["mips"])

                    # پیدا کردن خود تسک در workflow
                    runtime = None
                    for task in edge[devnumb]["workflow"]:
                        if task[0]["id"] == task_id:
                            runtime = task[0]["runtime"]
                            break

                    if runtime is None or mips is None:
                        continue

                    total_result += self.calculate_makespan(runtime, mips)
                    break  # از حلقه edgeها خارج شو

        return total_result

    def calculate_makespan(self, task_runtime, resource_mips):
        temp = EX()
        process_time = temp.Time_exec(task_runtime, resource_mips)

        self.MSmax = max(self.MSmax, process_time)
        self.MSmin = min(self.MSmin, process_time)

        if self.MSmax == self.MSmin:
            return 0.0
        return (process_time - self.MSmin) / (self.MSmax - self.MSmin)

    def calculate_new_velocity(self, velocity, pbest, position, gbest):
        inertia = self.W * velocity
        cognitive = self.c1 * random.uniform(0, 1) * (pbest - position)
        social = self.c2 * random.uniform(0, 1) * (gbest - position)
        return inertia + cognitive + social
