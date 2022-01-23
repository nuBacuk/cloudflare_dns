import sys
import CloudFlare


def dict_update(args,dns_records):
    for arg in sys.argv[1:]:
        args.update({arg.split("=")[0]: arg.split("=")[1]})
    try:
        dns_records.update({'name': args['CF_RECORD'], 'type': args['CF_RECORD_TYPE'], 'content': args['CF_RECORD_IP']})
    except KeyError as e:
        exit('Need arg %s' % e)


def get_record_id(cf, args):
    dns_records = cf.zones.dns_records.get(args['CF_ZONE_ID'])
    for record in dns_records:
        if record['name'] == args['CF_RECORD']:
            return args.update({"CF_RECORD_ID": record['id']})


def main():
    if sys.argv[1:]:
        args, dns_record = {}, {}
        dict_update(args, dns_record)
        cf = CloudFlare.CloudFlare(token=args['CF_TOKEN'])
        get_record_id(cf, args)
        if args['CF_RECORD_ID'] is not None:
            r = cf.zones.dns_records.patch(args['CF_ZONE_ID'], args['CF_RECORD_ID'], data=dns_record)
            return print("Record %s updated." % args['CF_RECORD'])
        else:
            r = cf.zones.dns_records.post(args['CF_ZONE_ID'], data=dns_record)
            return print("Record %s created." % args['CF_RECORD'])
    else:
        print("Need added args.\nExample: \n "
              "dns.py CF_TOKEN=123 CF_ZONE_ID=123 CF_RECORD=build.example.com CF_RECORD_TYPE=A CF_RECORD_IP=127.0.0.1")


if __name__ == '__main__':
    main()
