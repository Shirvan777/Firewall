from email.policy import default
from random import choices
from statistics import mode
from telnetlib import IP
from unittest.util import _MAX_LENGTH
from django.db import models
import ipaddress
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_ipv4_address,MaxValueValidator,MinValueValidator,MaxLengthValidator

'''ADD RULES HISSESINDEKI PARAMETRLERI RULES CEDVELINE ELAVE ETMEK UCUN MODEL'''
class Rules(models.Model):
    ICMP = 'ICMPv4:8'
    IP = '41'
    UDP = 'UDP'
    TCP = 'TCP'
    Allow = "Allow"
    Block = 'Block'
    IN = 'in'
    OUT = 'out'


    PROTOCOL_TYPES = (
        (ICMP, 'ICMPv4 - ECHO'),
        (IP, 'IPv6'),
        (UDP, 'UDP'),
        (TCP, 'TCP')      
    )
    ACTION = (
        (Allow, 'Allow'),
        (Block, 'Block')
    )
    DIR = (
        (IN, 'Inbound'),
        (OUT, 'Outbound')
    )
    
    source_ip = models.CharField(max_length=15,validators=[validate_ipv4_address])
    dest_ip = models.CharField(max_length = 15,validators=[validate_ipv4_address])
    source_port = models.PositiveIntegerField(validators=[
            MaxValueValidator(65635),
            MinValueValidator(1),
        ],default=1)
    dest_port = models.PositiveIntegerField(validators=[
            MaxValueValidator(65635),
            MinValueValidator(1),
        ],default=1)
    
    PROTOCOL_TYPES = models.CharField(max_length = 10,choices = PROTOCOL_TYPES)
    ACTION = models.CharField(max_length = 10,choices = ACTION)
    DIR = models.CharField(max_length=15, choices=DIR)

    class Meta:  
        db_table = "Rules"