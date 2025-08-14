from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name


class IDC(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City, related_name='idcs', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "city")

    def __str__(self) -> str:
        return f"{self.city}-{self.name}"


class Host(models.Model):
    hostname = models.CharField(max_length=128)
    ip = models.GenericIPAddressField(protocol='IPv4')
    city = models.ForeignKey(City, related_name='hosts', on_delete=models.PROTECT)
    idc = models.ForeignKey(IDC, related_name='hosts', on_delete=models.PROTECT)
    root_password_encrypted = models.TextField()
    password_updated_at = models.DateTimeField(auto_now=True)
    ping_last_ok = models.BooleanField(default=False)
    ping_last_rtt_ms = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("hostname", "ip")

    def __str__(self) -> str:
        return f"{self.hostname}({self.ip})"


class HostStats(models.Model):
    stat_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)
    host_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("stat_date", "city", "idc")

    def __str__(self) -> str:
        return f"{self.stat_date} {self.city}-{self.idc}: {self.host_count}"
