# Rights and Permissions
SerialBox defines discrete rights to *add*, *change* and *delete*
any given `Pool` or `SequentialRegion`.  This allows you to fine
tune what users, if any, have rights to perform those actions.

## Pools and Regions

The following *permissions* are available for each user accessing the
SerialBox API.

### Pool Permissions

* `add_pool` - can add new pools to the system.
* `change_pool` - can change existing poools.
* `delete_pool` - can delete existing pools.

### SequentialRegion Permissions

* `add_sequentialregion` - can add new sequential regions.
* `change_sequentialregion` - can change sequential regions.
* `delete_sequentialregion` - can delete existing sequential regions.

## Allocate API

The `Allocate API` has a single permission that can be assigned
to any given user that allows that user to allocate numbers.

* `allocate_numbers`: This gives a user rights to call the allocate API
and generate new numbers.

# Default Groups

The *SerialBox* module comes with a *Django Management Command* that
enables the creation of some default groups that quickly allow you
to give users certain umbrella rights over the API:

## *Pool API Access* Group

The *Pool API Access* group has full rights to create, change and
delete all `Pool`s and `SequentialRegion`s as well as access to the
`Allocate API`

## *Allocate Numbers Access* Group

This group gives any users within it the right to call the
`Allocate API` and create new numbers from Pools.

As part of the installation, you should have executed the management
command...but here it is again:

    python manage.py load_serialbox_auth



