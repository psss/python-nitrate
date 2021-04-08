Name: python-nitrate
Version: 1.7
Release: 1%{?dist}

Summary: Python API for the Nitrate test case management system
License: LGPLv2+

URL: https://github.com/psss/python-nitrate
Source0: %{url}/releases/download/%{version}/%{name}-%{version}.tar.bz2

# Depending on the distro, we set some defaults.
# Note that the bcond macros are named for the CLI option they create.
# "%%bcond_without" means "ENABLE by default and create a --without option"

# Fedora or RHEL 8+
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_with oldreqs
%bcond_with englocale
%else
# The automatic runtime dependency generator doesn't exist yet
%bcond_without oldreqs
# The C.UTF-8 locale doesn't exist, Python defaults to C (ASCII)
%bcond_without englocale
%endif

# For older Fedora and RHEL build python2-nitrate as well
%if 0%{?fedora} > 31 || 0%{?rhel} > 7
%bcond_with python2
%else
%bcond_without python2
%endif

BuildArch: noarch
BuildRequires: git-core
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-six
%if %{with python2}
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-six
%endif

%{?python_enable_dependency_generator}

%global _description %{expand:
A Python interface to the Nitrate test case management system.
The package consists of a high-level Python module (provides
natural object interface), a low-level driver (allows to directly
access Nitrate XMLRPC API) and a command line interpreter (useful
for fast debugging and experimenting).}

%description %_description


# Python 2
%if %{with python2}
%package -n python2-nitrate
Summary: %{summary}
%{?python_provide:%python_provide python2-nitrate}
%if %{with oldreqs}
%if 0%{?rhel} > 7
Requires: python2-gssapi
Requires: python2-psycopg2
%else
Requires: python-gssapi
Requires: python-psycopg2
%endif
Requires: python2-six
%endif

%description -n python2-nitrate %_description
%endif

# Python 3
%package -n python%{python3_pkgversion}-nitrate
Summary: %{summary}
%{?python_provide:%python_provide python3-nitrate}
%if %{with oldreqs}
Requires: python%{python3_pkgversion}-gssapi
Requires: python%{python3_pkgversion}-psycopg2
Requires: python%{python3_pkgversion}-six
%endif
Conflicts: python2-nitrate < 1.5-3

%description -n python%{python3_pkgversion}-nitrate %_description

%prep
%autosetup -S git

%build
%if %{with englocale}
export LANG=en_US.utf-8
%endif
%if %{with python2}
%py2_build
%endif
%py3_build

%install
%if %{with englocale}
export LANG=en_US.utf-8
%endif
%if %{with python2}
%py2_install
%endif
%py3_install
mkdir -p %{buildroot}%{_mandir}/man1
install -pm 644 docs/*.1.gz %{buildroot}%{_mandir}/man1
# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1335203
pathfix.py -pni "%{__python3} %{py3_shbang_opts}i" %{buildroot}%{_bindir}/nitrate

%if %{with python2}
%files -n python2-nitrate
%{python2_sitelib}/nitrate/
%{python2_sitelib}/nitrate-*.egg-info/
%license LICENSE
%endif

%files -n python%{python3_pkgversion}-nitrate
%{python3_sitelib}/nitrate/
%{python3_sitelib}/nitrate-*.egg-info/
%{_mandir}/man1/*
%{_bindir}/nitrate
%doc README examples
%license LICENSE

%changelog
* Wed Apr 07 2021 Martin Zelený <mzeleny@redhat.com> - 1.7-1
- Fix float as a parameter of the listed() function
- Solve DeprecationWarning
- Make examples usable with Python 3
- Enable copr builds on commits in the master branch
- Merge the Packit config and Makefile changes
- Enable custom create archive for packit
- Porting cache.py to Python 3

* Tue Jun 09 2020 Petr Šplíchal <psplicha@redhat.com> - 1.6-1
- Handle wrongly encoded messages in log [fix #20]
- Make teiid Python 3 compatible [fix #13]
- Better solving the do_command() bug
- Bringing back eval() - workaround for XMLRPC
- Output nicer tracebacks on connection failures
- Enable automated python dependecies generator
- Last spec file changes for RHEL7 (hopefully)
- For older releases build both python2 and python3

* Thu Nov 21 2019 Petr Šplíchal <psplicha@redhat.com> - 1.5-4
- Fix requires (no python2-gssapi and python2-psycopg2 in RHEL7).
- Enable automated python dependecies generator

* Wed Nov 20 2019 Petr Šplíchal <psplicha@redhat.com> - 1.5-3
- For older releases build both python2 and python3 packages
- Include conflicting files only in the python3 package

* Mon Nov 11 2019 Petr Šplíchal <psplicha@redhat.com> - 1.5-2
- Use py3_build and py3_install to simplify spec
- Rename and explicitly list the license file
- Remove group, fix license, add missing requires

* Mon Nov 04 2019 Martin Zeleny <mzeleny@redhat.com> 1.5-0
- Ported to Python 3

* Mon Nov 05 2018 Petr Šplíchal <psssssss@gmail.com> 1.4-1
- Update specfile to new python packaging standards
- Performance improvement for TestPlan.sortkey
- Port to python-gssapi from pykerberos
- Make TestRun errata_id default to None

* Tue May 10 2016 Martin Frodl <mfrodl@redhat.com> 1.3-2
- Removed obsolete project page links

* Tue Feb 09 2016 Petr Šplíchal <psplicha@redhat.com> 1.3-1
- Package nitrate for PyPI, several adjustments, docs update
- Better handle non-existent objects [BZ#1204028]
- Correctly handle no caseplan found [BZ#1171671]
- Typo fix in the TestPlan's _attributes [BZ#1304295]
- Make sure that PlanStatus id type is int

* Fri Aug 08 2014 Petr Šplíchal <psplicha@redhat.com> 1.2-0
- Include example config in documentation [BZ#1098818]
- Handle duplicate entry errors gracefully [BZ#1112521]
- Added Aleš Zelinka to the list of contributors

* Sat May 17 2014 Petr Šplíchal <psplicha@redhat.com> 1.1-0
- TestCase.{setup,action,effect,breakdown} attributes [BZ#1089039]
- Map automated/manual when searching test cases [BZ#1092464]
- Iterate over PlanRuns sorted by id/creation
- Indexing support for containers
- Separate methods for locking, handle corrupted cache
- Limit cache writing window (chance of corruption) [BZ#1091404]
- Ignore malformed and stale cache locks [BZ#1091404]
- Workaround Teiid problem with converting time [BZ#1093054]

* Fri Apr 11 2014 Petr Šplíchal <psplicha@redhat.com> 1.0-0
- New stable version, see release notes for the list of changes
- http://psss.fedorapeople.org/python-nitrate/notes.html

* Wed Apr 09 2014 Petr Šplíchal <psplicha@redhat.com> 0.15-0
- Single LOG_DATA level for data-related logs, docs cleanup
- Initialize all plan-case tags in CACHE_OBJECTS level
- Do not use log.error during object creation/init
- Raise exception when invalid Build name given
- Added link to the Copr repository
- Use object name for identifier if id is unknown
- Containers with uncached items should expire as well
- No all-items fetching for modified containers [BZ#1084563]

* Fri Apr 04 2014 Petr Šplíchal <psplicha@redhat.com> 0.14-0
- Allow wiping cache of subclasses of given class
- Update TestRun's CaseRuns in MultiCall batches
- Import all containers into the main nitrate module
- Remove version from test-bed-prepare Product init
- Display warn message about locked persistent cache
- Document batch updates using Cache().update()
- Summary of new features added to release notes
- Add reference to release notes and individual module docs
- Custom formatter should return unicode messages
- Updated the create.py simple example code
- Test suite documentation update
- Use tag name for hashing to allow creating new tags
- Initial version of the release notes

* Thu Apr 03 2014 Petr Šplíchal <psplicha@redhat.com> 0.13-0
- Give a summary of expired items for easier debugging
- Wake up only containers with already cached items
- New log.all() method for super-detailed logging
- Use singletons for Coloring and Caching configuration
- Use a single Cache instance for persistent cache handling
- Include minimal config example in the synopsis
- Use custom concise test results for python 2.7+ only
- New log level for Teiid, global constants for all levels
- Explicitly mention cache levels for environment variable
- Use Config class directly rather than through Nitrate
- Teiid requires python-psycopg2 for db connection
- Refactored the huge api module into several modules
- Explicitly mention the update() method in examples
- Ignore enter() and exit() when persistent caching off

* Wed Mar 26 2014 Petr Šplíchal <psplicha@redhat.com> 0.12-0
- Disable PlanComponents test until BZ#866974 is fixed.
- Support for fetching data from a Teiid instance
- Simple locking for persistent cache implemented
- Support for string tags (backward-compatible)
- Use multicall for unlinking testcases from testplans
- Containers should iterate over sorted test cases
- Support for test case sortkey in test plans [BZ#869594]
- Improved logging for Container add/remove methods
- Internal utility function for idifying
- Cache.update() support for multicall slicing
- Status can be specified upon test case creation
- New utility function sliced() for cutting loafs
- Store the initial object dict for future use
- Setting arguments/requirement upon test case creation [BZ#1032259]
- Product property removed from the TestCase class [BZ#1076058]
- Special handling for comparison with None
- TestRun.caseruns and TestRun.testcases containers
- Cache setup only when needed, improved cleanup logging
- Make sure we always compare objects of the same type
- Improved container initialization when inject given
- TestPlan.testruns reimplemented using PlanRuns container
- More debugging output when expiring objects from cache
- Containers should always be read-only properties
- PlanComponents container implemented

* Fri Mar 7 2014 Petr Šplíchal <psplicha@redhat.com> 0.11-0
- One year is good enough for never-expire limit
- Bugs reimplemented with containers and caching
- Wake up containers as sets of objects, not lists
- Use empty cache for objects not found in the cache file
- Identifier should show UNKNOWN when id not defined
- Set the default command line editing mode to vi
- Do not use root logger for nitrate logging [BZ#1060206]
- Use NitrateError class for raising exceptions instead of plain str
- Fix regression after version removal from product
- Container implementation status documented
- TestRun.started and TestRun.finished [BZ#957741]
- Better document the update() method [BZ#1004434]
- New attribute TestPlan.owner [BZ#954913]
- Move the default version from Product into TestPlan
- Version fetch cleanup & test improvements
- Use custom result format for unit tests
- Added TestCase.created attribute (creation date) [BZ#1008489]

* Wed Sep 25 2013 Petr Šplíchal <psplicha@redhat.com> 0.10-0
- Add Filip Holec to the list of contributors
- Convert timedelta into a human readable format
- The Big Cleanup of Ininitialization and Caching
- New custom log levels for cache and xmlrpc
- Component should be among exported classes
- Added support for plain authentication
- Initialize color mode before caching
- Colored logging [BZ#965665]
- Handle attribute init and fetch timestamp reset at one place
- Test summary should report errors as well
- No need to load cache when testing
- Allow to clear cache for selected classes only
- Give an overall test summary at the end of testing
- Support cache expiration configuration for parent classes
- Improved auto-plural in listed() for words ending with 's'
- New utility function header() for printing simple headers
- Object fetching cleanup and improved _is_cached()
- Move server communication debugging to lower level
- New method Cache.update() for group updates
- Use temporary cache file for running the test suite
- Correctly handle modified objects with caching
- Fix problem with restoring containers from the cache
- Document logging with custom level, some cleanup
- Common identifier width handling
- Move constants to the top, expiration adjustments
- Persistent caching for all Container classes
- Container initialization
- Persistent cache implementation
- Common caching support in the Nitrate class
- Skip performance tests when in regular mode
- MultiCall support
- Tag class implementation
- Performance test cases
- Test bed prepare script
- Make the newline in info() optional
- Added support for performance tests (--performance)
- Allow short PlanType initialization by string
- Allow to set the reference link upon test case creation [BZ#843382]

* Mon Dec 10 2012 Petr Šplíchal <psplicha@redhat.com> 0.9-0
- New function unlisted() for conversion from human readable list
- Clean up the cache before testing caching
- Fix test plan initialization by type name
- Rename test case components container to CaseComponents
- Implemented TestPlan.children property [BZ#863226]
- Allow to select cases when creating a new run [BZ#863480]
- Invalid category should raise Nitrate exception [BZ#862523]
- Implement PlanType using XMLRPC instead of hard coded values [BZ#841299]
- Cleanup of log, cache and color funtions
- Use unicode for logging where necessary [BZ#865033]
- Use unicode for logging in _setter() [BZ#865033]
- Sane unicode representation for user with no name [BZ#821629]
- Support for system-wide config in /etc/nitrate.conf [BZ#844363]
- Remove *.pyc files as well when cleaning
- Move global variables out of the functions
- Move utils tests into a separate class
- Document how to get a short Nitrate summary [BZ#883798]
- Push files to the production web only when in the master branch
- New TestCase reference link field [BZ#843382]
- Forgotten 'notes' in the list of test case attributes
- Don't forget to include errata id when creating a new test run
- Fix test run errata update, improve the self test
- Added errata field in class TestRun
- Suggest https in the minimal config example
- Test case automation flags cleanup
- Empty script or arguments to be handled same as None
- Smarter implementation of the listed() function

* Wed Feb 29 2012 Petr Šplíchal <psplicha@redhat.com> - 0.8-0
- New method clear() for cleaning containers
- Component and Components class implementation
- Improved object initialization and id check

* Wed Feb 22 2012 Petr Šplíchal <psplicha@redhat.com> - 0.7-2
- Fix url, directory ownership and preserve timestamps.

* Wed Feb 22 2012 Petr Šplíchal <psplicha@redhat.com> 0.7-1
- Initial packaging.
